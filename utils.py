from telegram import User
import config


def is_chinesse(c):
    """
    Returns True if the character passed as parameter is a Chinesse
    one.
    """
    num = ord(c)
    return any((
        0x2E80 <= num <= 0x2FD5,
        0x3190 <= num <= 0x319F,
        0x3400 <= num <= 0x4DBF,
        0x4E00 <= num <= 0x9FCC,
        0x6300 <= num <= 0x77FF,
        ))


def too_much_chinesse_chars(s):
    letters = list(s)
    num_chinesse_chars = sum([is_chinesse(c) for c in letters])
    percent = num_chinesse_chars / len(letters)
    return percent > config.CHINESSE_CHARS_MAX_PERCENT  # More than allowed
                                                        # chars are chinesse


def is_valid_name(user: User):
    return len(user.first_name) <= config.MAXLEN_FOR_USERNAME_TO_TREAT_AS_HUMAN


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
    return any((
        not is_valid_name(user),
        too_much_chinesse_chars(user.first_name),
        is_tgmember_sect(user.first_name),
        ))
