"""All tests gathers here.
"""
from envget import base


def test_parse_osenvparse() -> None:
    """Basic test.
    """
    base.env("DEBUGME")
