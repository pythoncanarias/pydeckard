import functools
import datetime
import grp
import platform
import pwd
import random
import re
import sys
from pathlib import Path
from typing import Tuple, Optional, NamedTuple

from telegram import User
from pydeckard import config


def is_chinese(c):
    """
    Returns True if the character passed as parameter is a Chinese one
    """
    num = ord(c)
    return any(
        (
            0x2E80 <= num <= 0x2FD5,
            0x3190 <= num <= 0x319F,
            0x3400 <= num <= 0x4DBF,
            0x4E00 <= num <= 0x9FCC,
            0x6300 <= num <= 0x77FF,
        )
    )


def too_much_chinese_chars(s):
    letters = list(s)
    num_chinese_chars = sum([is_chinese(c) for c in letters])
    percent = num_chinese_chars / len(letters)
    # More than allowed chars are Chinese
    return percent > config.MAX_CHINESE_CHARS_PERCENT


def is_valid_name(user: User):
    return len(user.first_name) <= config.MAX_HUMAN_USERNAME_LENGTH


def is_tgmember_sect(first_name: str):
    return "tgmember.com" in first_name.lower()


def is_bot(user: User):
    """
    Returns True if a new user is a bot. So far only the length of the
    username is checked. In the future, we can add more conditions and use a
    score/weight of the probability of being a bot.

    :param user: The new User
    :type user: User
    :return: True if the new user is considered a bot (according to our rules)
    :rtype: bool
    """
    # Add all the checks that you consider necessary
    return any(
        (
            not is_valid_name(user),
            too_much_chinese_chars(user.first_name),
            is_tgmember_sect(user.first_name),
        )
    )


@functools.lru_cache()
def get_reply_regex(trigger_words: Tuple[str]):
    """
    Build a regex to match on the trigger words
    """
    pattern = "|".join([fr"\b{word}\b" for word in trigger_words])
    return re.compile(pattern, re.IGNORECASE)


def bot_wants_to_reply() -> bool:
    return random.random() < config.VERBOSITY


class BotReplySpec(NamedTuple):
    message: str
    trigger: str
    reply: str


def triggers_reply(message: str) -> Optional[BotReplySpec]:
    for trigger_words, bot_reply in config.REPLIES.items():
        regex = get_reply_regex(trigger_words)
        match = regex.search(message)
        if match is not None and bot_wants_to_reply():
            # When a match is found, check if the bot will reply based on its
            # reply likelihood
            if not isinstance(bot_reply, str):
                # If value is a list then pick random string from
                # multiple values:
                bot_reply = random.choice(bot_reply)
            return BotReplySpec(message, match.group(0), bot_reply)
    return None


def pluralise(number: int, singular: str, plural: Optional[str] = None) -> str:
    if plural is None:
        plural = f"{singular}s"
    return singular if number == 1 else plural


def since(reference) -> str:
    """Returns a textual description of time passed.

    Parameter:
     - reference: datetime is the datetime used to get the difference
        ir delta.
    """

    dt = datetime.datetime.now()
    delta = dt - reference
    buff = []
    days = delta.days
    if days:
        buff.append(f"{days} {pluralise(days, 'day')}")
    seconds = delta.seconds
    if seconds > 3600:
        hours = seconds // 3600
        buff.append(f"{hours} {pluralise(hours, 'hour')}")
        seconds %= 3600
    minutes = seconds // 60
    if minutes > 0:
        buff.append(f"{minutes} {pluralise(minutes, 'minute')}")
    seconds %= 60
    buff.append(f"{seconds} {pluralise(seconds, 'second')}")
    return " ".join(buff)


def validate_input(prompt_head, acceptable=None, typus=None):
    """
    This function is designed to capture the parameters that will be used to configure the bot.
    It captures input and validates the data obtained.
    Steps:
        Create a text string to use as a prompt.
        Request the input.
        Validate the received data.
        Return the validated data or None.
    Parameter capture can be interrupted with Ctrl+C

    Arguments
        prompt_head (str): Start of the message to be displayed to the user.
        acceptable (list/tuple, optional): Whitelist of values or range (min, max).
        typus (callable): Data type to convert the input to.

    Return
        The data validated and converted to type 'typus' or None
    """

    prompt_tail = ''

    if isinstance(acceptable, list):
        prompt_tail = f" ({'/'.join(map(str, acceptable))})"
    elif isinstance(acceptable, tuple):
        prompt_tail = f' ({acceptable[0]}-{acceptable[1]})'

    prompt = f'{prompt_head}{prompt_tail}: '

    while True:
        try:
            data = input(prompt).strip()
        except KeyboardInterrupt:
            raise

        if not (data and callable(typus)):
            return None

        try:
            if typus is int:
                data = int(data, 0)
            elif typus is str and acceptable and all(x.isupper() for x in acceptable):
                data = data.upper()
            elif typus is str or typus is float:
                data = typus(data)
            else:
                return None
        except ValueError:
            print(f'El valor debe ser de tipo {typus.__name__}')
            continue

        if isinstance(acceptable, list) and data not in acceptable:
            print(f'El valor debe ser una de estas opciones: {"/".join(map(str, acceptable))}')
            continue

        if isinstance(acceptable, tuple):
            if not (acceptable[0] <= data <= acceptable[1]):
                print(f'El valor debe estar entre {acceptable[0]} y {acceptable[1]}.')
                continue

        return data


def setup_bot():
    """
    A wizard starts to configure the bot and create an automatic startup system based on the operating system.
    It performs an input for each required configuration parameter.
    The "parameters" list contains all the defined parameters, each as a tuple of four elements:
        parameter name,
        prompt for input,
        a tuple with two values to indicate a range of allowed values OR a list with values to indicate the
        different allowed options OR None,
        a class to cast the value to the allowed type
    """

    root_path = Path(sys.prefix)
    bin_path = Path(sys.executable).parent
    bot_executable = bin_path / 'bot'
    env_path = root_path / '.env'
    system_name = platform.system()

    print(f'\n--- Asistente de configuración para PyDeckard (SO: {system_name}) ---\n\n')

    parameters = [('TELEGRAM_BOT_TOKEN', 'Introduzca el Token del Bot', None, str),
                  ('VERBOSITY', 'Nivel de verbosidad', (0.0, 1.0), float),
                  ('LOG_LEVEL', 'Nivel de registro de logs', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], str),
                  ('POLL_INTERVAL', 'Intervalo de polling para la API de Telegram', (1, 10), int),
                  ('BOT_GREETING', 'Saludo del bot', None, str),
                  ('MAX_HUMAN_USERNAME_LENGTH', 'Longitud máxima del username', None, int),
                  ('MAX_CHINESE_CHARS_PERCENT', 'Máximo porcentaje de caracteres chinos en username',
                   (0.0, 1.0), float),
                  ('WELCOME_DELAY', 'Tiempo de retardo para la bienvenida (seg)', None, int), ]

    try:
        items_env = {key: validate_input(*args) for key, *args in parameters}
    except KeyboardInterrupt:
        print('Asistente cancelado por el usuario.')
        sys.exit(1)

    with open(env_path, 'w') as fout:
        lines = [f'{key}={value}\n' for key, value in items_env.items() if value]
        fout.writelines(lines)

    print(f'\n\nArchivo .env creado en {root_path}')

    if system_name == 'Linux':
        stat_info = root_path.stat()

        user_name = pwd.getpwuid(stat_info.st_uid).pw_name
        group_name = grp.getgrgid(stat_info.st_gid).gr_name

        service_path = root_path / 'pydeckard.service'

        service_content = f"""[Unit]
Description=PyDeckard
After=network.target

[Service]
Type=simple
User={user_name}
Group={group_name}
WorkingDirectory={root_path}
ExecStart={bot_executable}
Environment=PYTHONUNBUFFERED=1
Restart=always

[Install]
WantedBy=multi-user.target
Alias=PyDeckard.service
"""

        with open(service_path, 'w') as f:
            f.write(service_content)

        print(f'\nArchivo pydeckard.service creado en {root_path}')

        print(f'\nPara configurar, activar e iniciar el service en systemd ejecute los siguientes comandos:')

        print(f'\nsudo cp {service_path} /etc/systemd/system/')
        print('sudo systemctl daemon-reload')
        print('sudo systemctl enable --now pydeckard')

        sys.exit(0)

    elif system_name == 'Darwin':
        print('Entorno macOS detectado, configuración realizada, pregúntele a Apple® como arrancarlo.')
        sys.exit(1)

    elif system_name == 'Windows':
        print('Entorno Windows detectado, configuración realizada, pregúntele a Microsoft® como arrancarlo.')
        sys.exit(1)

    elif system_name == 'Java':
        print('Entorno Jython detectado. Usted mismo.')
        sys.exit(1)

