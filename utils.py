from telegram import User

USERNAME_MAX_LENGTH = 100


def is_bot(user: User):
    """
    Returns true if a new username is a bot. For now only the length of the username is checked.
    In the future, we can add more functions and use a score/weight of the probability of being a bot

    :param user: The new User
    :type user: User
    :return: True if the new user is considered a bot (according to our rules)
    :rtype: bool
    """
    # Add all the checks that you consider necessary

    return check_username(user)


def check_username(user: User):
    return True if len(user.name) > USERNAME_MAX_LENGTH else False
