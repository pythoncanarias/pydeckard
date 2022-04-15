import functools
import datetime
import random
import re
from typing import Tuple, Optional, NamedTuple

from telegram import User
import settings


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


def is_tgmember_sect(first_name: str):
    return "tgmember.com" in first_name.lower()


@functools.lru_cache()
def get_reply_regex(trigger_words: Tuple[str]):
    """
    Build a regex to match on the trigger words
    """
    pattern = "|".join([fr"\b{word}\b" for word in trigger_words])
    return re.compile(pattern, re.I)


def bot_wants_to_reply() -> bool:
    return random.random() < settings.VERBOSITY


class BotReplySpec(NamedTuple):
    message: str
    trigger: str
    reply: str


def triggers_reply(message: str) -> Optional[BotReplySpec]:
    for trigger_words, bot_reply in settings.REPLIES.items():
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


def since(dt=None, reference=datetime.datetime.now()) -> str:
    """Returns a textual description of time passed.

    Parameters:

     - dt: datetime is the date to calculate the difference from
           reference. If not used, take the value from the current
           datetime.

     - reference: datetime is the datetime used to get the difference
        ir delta. If not defined, default value is since the definition
        of the function, this is,since the moment the current run of the
        program started.
    """
    dt = dt or datetime.datetime.now()
    delta = dt - reference
    buff = []
    days = delta.days
    if days:
        buff.append(f"{days} {pluralise(days, 'day')}")
    seconds = delta.seconds
    if seconds > 3600:
        hours = seconds // 3600
        buff.append(f"{hours} {pluralise(hours, 'hour')}")
        seconds = seconds % 3600
    minutes = seconds // 60
    if minutes > 0:
        buff.append(f"{minutes} {pluralise(minutes, 'minute')}")
    seconds = seconds % 60
    buff.append(f"{seconds} {pluralise(seconds, 'second')}")
    return " ".join(buff)
