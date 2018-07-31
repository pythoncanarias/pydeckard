from prettyconf import config

TELEGRAM_BOT_TOKEN = config(
    "TELEGRAM_BOT_TOKEN",
    default="put here the token of your bot"
)

# bot verbosity (0 ... 1)
VERBOSITY = 0.33

PYZEN = [
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

REPLY = {
    ("java",): "BIBA JABA!! ☕️",
    ("cobol",): "BIBA KOBOL!! 💾",
    ("javascript",): "BIBA JABAESKRIPT!! 🔮",
    ("php",): "BIBA PEHACHEPÉ!! ⛱",
    ("he visto", "has visto", "han visto", "visteis", "vieron", "vi"):
        "Yo he visto cosas que vosotros no creeríais. Atacar naves en llamas "
        "más allá de Orión. He visto Rayos-C brillar en la oscuridad cerca de "
        "la puerta de Tannhäuser. Todos esos momentos se perderán en el "
        "tiempo... como lágrimas en la lluvia. Es hora de morir. 🔫",
    ("python", "pitón", "piton"): PYZEN,
}

MAXLEN_FOR_USERNAME_TO_TREAT_AS_HUMAN = 100
