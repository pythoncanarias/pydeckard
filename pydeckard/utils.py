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

def setup_bot():
    """
    Arranca un asistente para la configuración del bot y la creación de un sistema de arranque automáquico
    por el sistema operativo
    """

    root_path = Path(sys.prefix)
    bin_path = Path(sys.executable).parent
    bot_executable = bin_path / 'bot'

    env_path = root_path / '.env'

    system_name = platform.system()
    print(f"--- Asistente de configuración para PyDeckard (SO: {system_name}) ---")

    token = input('Introduzca el Token del Bot: ')
    welcome_delay = input('Introduzca el retardo para la bienvenida: ')
    chinese_chars = input('Porcentaje de caracteres chinos en username (0.0-1.0): ')
    username_length = input('Longitud máxima del username: ')
    greeting = input('Saludo del bot: ')
    poll_interval = input('Intervalo de polling para la API de Telegram: ')
    log_level = input('Nivel de registro de logs: ')
    verbosity = input('Nivel de verbosidad: ')

    with open(env_path, 'w') as f:
        f.write(f'VERBOSITY={verbosity}\n')
        f.write(f'LOG_LEVEL={log_level}\n')
        f.write(f'POLL_INTERVAL={poll_interval}\n')
        f.write(f'BOT_GREETING ={greeting}\n')
        f.write(f'MAX_HUMAN_USERNAME_LENGTH={username_length}\n')
        f.write(f'CHINESE_CHARS={chinese_chars}\n')
        f.write(f'WELCOME_DELAY={welcome_delay}\n')





    MAXLEN_FOR_USERNAME_TO_TREAT_AS_HUMAN = 100
    CHINESE_CHARS_MAX_PERCENT = 0.15











    print(f"✅ Archivo .env creado en {root_path}")

    if system_name == "Linux":
        setup_linux(root_path, bot_executable)



    stat_info = root_path.stat()

    user_name = pwd.getpwuid(stat_info.st_uid).pw_name
    group_name = grp.getgrgid(stat_info.st_gid).gr_name

    # Archivos destino

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

    print(f'✅ Archivo pydeckard.service creado en {root_path}')
    print('\nA continuación debe copiar el archivo pydeckard.service a /etc/systemd/system/, activar el '
          'servicio y ejecutarlo')
    print(f'sudo cp {service_path} /etc/systemd/system/')
    print('sudo systemctl daemon-reload')
    print('sudo systemctl enable --now pydeckard')

    sys.exit(0)
