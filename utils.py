from telegram import User
import config


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
    return not is_valid_name(user)


def is_valid_name(user: User):
    return len(user.first_name) <= config.MAXLEN_FOR_USERNAME_TO_TREAT_AS_HUMAN
