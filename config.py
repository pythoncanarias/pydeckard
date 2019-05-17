from prettyconf import config

TELEGRAM_BOT_TOKEN = config(
    "TELEGRAM_BOT_TOKEN",
    default="put here the token of your bot"
)

# How likely is the bot to be triggered by one of the patterns it recognises.
# - Allowed values: A float from 0 to 1 (0 will disable bot replies)
VERBOSITY = config("BOT_VERBOSITY", float, default=0.33)


# Log level, default is WARNING
LOG_LEVEL = config('LOG_LEVEL', default='WARNING')

# Poll interval for telegram API request, default is 3 seconds
POLL_INTERVAL = config('POLL_INTERVAL', int, default=3)

# Bot message for start command
BOT_GREETING = "Hi! I'm a friendly, sligthly psychopath robot"

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
