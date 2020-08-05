"""Exceptions."""


class IncorrectDotenvPath(Exception):
    """If .env file doesnt exists."""


class NotSettedDotenvPath(Exception):
    """If .env file doesnt set."""


class BrokenDotenvStructure(Exception):
    """If .env has broken structure."""
