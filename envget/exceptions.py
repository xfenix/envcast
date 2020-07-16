"""Exceptions.
"""


class IncorrectDotenvPath(Exception):
    """If .env file doesnt exists.
    """

    pass


class NotSettedDotenvPath(Exception):
    """If .env file doesnt set.
    """

    pass
