"""All tests gathers here.
"""
from __future__ import annotations
import decimal
import pathlib
import typing
import random
from unittest import mock

import pytest
import faker

from envget import base


FAKE_GEN: faker.Faker = faker.Faker()
FAKE_TYPES_MAP: dict = {
    str: lambda: FAKE_GEN.pystr(),
    int: lambda: FAKE_GEN.pyint(),
    float: lambda: FAKE_GEN.pyfloat(),
    bool: lambda: random.choice(("1", "yEs", "oK", "True", "On", "oK  ", "false", "False", "NO", "Fake")),
    decimal.Decimal: lambda: FAKE_GEN.pydecimal(),
    pathlib.Path: lambda: pathlib.Path(FAKE_GEN.file_path()),
}


@pytest.mark.parametrize("desired_type", FAKE_TYPES_MAP.keys())
@pytest.mark.parametrize("key_exists", (True, False))
def test_parse_osgetenv_parse(monkeypatch, desired_type, key_exists) -> None:
    """Test for os.getenv provider.
    """
    env_key: str = f"DEBUGME_KOKOK_PRIVET_{FAKE_GEN.pystr()}"
    original_value: typing.Any = FAKE_TYPES_MAP[desired_type]()
    monkeypatch.setenv(env_key, str(original_value))
    casted_value_from_module: typing.Any = base.env(env_key if key_exists else FAKE_GEN.pystr(), type_cast=desired_type)
    if key_exists:
        if desired_type == bool:
            assert casted_value_from_module == bool(original_value.lower().strip() in base.BOOLEAN_VALUES)
        else:
            assert casted_value_from_module == original_value
    else:
        assert casted_value_from_module is None


@pytest.mark.parametrize("desired_type", FAKE_TYPES_MAP.keys())
def test_parse_dotenv_parse(monkeypatch, desired_type) -> None:
    """Test for .env file provider.
    """
    env_key: str = f"TEST_KEY_{FAKE_GEN.pystr()}"
    original_value: typing.Any = FAKE_TYPES_MAP[desired_type]()
    monkeypatch.setattr("pathlib.Path.read_text", mock.Mock(return_value=f"{env_key} = {original_value}\n"))
    casted_value_from_module: typing.Any = base.dotenv(env_key, type_cast=desired_type)
    if desired_type == bool:
        assert casted_value_from_module == bool(original_value.lower().strip() in base.BOOLEAN_VALUES)
    else:
        assert casted_value_from_module == original_value
