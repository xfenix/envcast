"""All tests gathers here.
"""
from __future__ import annotations
import decimal
import pathlib
import typing

import pytest
import faker

from envget import base


FAKE_GEN: faker.Faker = faker.Faker()
FAKE_TYPES_MAP: dict = {
    str: FAKE_GEN.pystr(),
    int: FAKE_GEN.pyint(),
    float: FAKE_GEN.pyfloat(),
    bool: FAKE_GEN.pybool(),
    decimal.Decimal: FAKE_GEN.pydecimal(),
    pathlib.Path: pathlib.Path(),
}


@pytest.mark.parametrize("type_cast", FAKE_TYPES_MAP.keys())
def test_parse_osenvparse(monkeypatch, type_cast) -> None:
    """Basic test.
    """
    env_key: str = f"DEBUGME_KOKOK_PRIVET_{FAKE_GEN.pystr()}"
    monkeypatch.setenv(env_key, str(FAKE_TYPES_MAP[type_cast]))
    base.env(env_key, type_cast)
