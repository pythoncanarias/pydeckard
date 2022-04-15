from typing import NamedTuple, Any

from decouple import config as _config



_config_registry = []


class _ConfigItem(NamedTuple):
    name: str
    value: Any
    suppress_log: bool = False

    def log(self, logger_method, indent=False):
        value = "***PRIVATE***" if self.suppress_log else self.value
        indentation = '   ' if indent else ''
        logger_method(f"{indentation}{self.name} = {value}")


def config(item, cast=lambda v: v, suppress_log=False, **kwargs):
    value = _config(item, cast, **kwargs)
    global _config_registry
    _config_registry.append(_ConfigItem(item, value, suppress_log))
    return value


def log(logger_method):
    logger_method("Bot configuration:")
    for config_item in _config_registry:
        config_item.log(logger_method, indent=True)


BOT_TOKEN = config(
    "TELEGRAM_BOT_TOKEN",
    default="put here the token of your bot",
    suppress_log=True
)

# How likely is the bot to be triggered by one of the patterns it recognises.
# - Allowed values: A float from 0 to 1 (0 will disable bot replies)
VERBOSITY = config("BOT_VERBOSITY", float, default=0.33)


# Log level, default is WARNING
LOG_LEVEL = config('LOG_LEVEL', default='WARNING')

# Poll interval for telegram API request, default is 3 seconds
POLL_INTERVAL = config('POLL_INTERVAL', int, default=3)

# Bot message for start command
BOT_GREETING = config('BOT_GREETING',
                      default="Hi! I'm a friendly, slightly psychopath robot")

# A username longer than this will be considered non-human
# - Allowed values: An integer larger than 1
MAX_HUMAN_USERNAME_LENGTH = config('MAX_HUMAN_USERNAME_LENGTH',
                                   int,
                                   default=100)


# We have found, through empiric evidence, that a large ration of Chinese
# characters usually indicates the user is a spammer or bot.
# This sets the maximum allowed percent of Chinese characters before
# considering the user a bot.
# - Allowed values: A float from 0 to 1
MAX_CHINESE_CHARS_PERCENT = config('MAX_CHINESE_CHARS_PERCENT',
                                   float,
                                   default=0.15)


# Delay (in seconds) to wait before sending welcome message. New users have
# 5 minutes to solve a captcha. The default delay is 5 and a half minutes.
WELCOME_DELAY = config('WELCOME_DELAY', int, default=10)


def bot_replies_enabled() -> bool:
    return VERBOSITY > 0


THE_ZEN_OF_PYTHON = [
    "Beautiful is better than ugly.",
    "Explicit is better than implicit.",
    "Simple is better than complex.",
    "Complex is better than complicated.",
    "Flat is better than nested.",
    "Sparse is better than dense.",
    "Readability counts.",
    "Special cases aren't special enough to break the rules.",
    "Although practicality beats purity.",
    "Errors should never pass silently.",
    "Unless explicitly silenced.",
    "In the face of ambiguity, refuse the temptation to guess.",
    "There should be one-- and preferably only one --obvious way to do it.",
    "Although that way may not be obvious at first unless you're Dutch.",
    "Now is better than never.",
    "Although never is often better than *right* now.",
    "If the implementation is hard to explain, it's a bad idea.",
    "If the implementation is easy to explain, it may be a good idea.",
    "Namespaces are one honking great idea -- let's do more of those!"
    ]


REPLIES = {
    ("java",): "BIBA JABA!! ☕️",
    ("cobol",): "BIBA KOBOL!! 💾",
    ("javascript",): "BIBA JABAESKRIPT!! 🔮",
    ("php",): "BIBA PEHACHEPÉ!! ⛱",
    ("he visto", "has visto", "han visto", "visteis", "vieron", "vi"):
        "Yo he visto cosas que vosotros no creeríais. Atacar naves en llamas "
        "más allá de Orión. He visto Rayos-C brillar en la oscuridad cerca de "
        "la puerta de Tannhäuser. Todos esos momentos se perderán en el "
        "tiempo... como lágrimas en la lluvia. Es hora de morir. 🔫",
    ("python", "pitón", "piton"): THE_ZEN_OF_PYTHON,
}

MAXLEN_FOR_USERNAME_TO_TREAT_AS_HUMAN = 100

CHINESE_CHARS_MAX_PERCENT = 0.15
