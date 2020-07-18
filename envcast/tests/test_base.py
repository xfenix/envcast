"""All tests gathers here.
"""
from __future__ import annotations
import typing
import random
import decimal
import pathlib
from unittest import mock

import pytest
import faker

import envcast
import envcast.base


FAKE_GEN: faker.Faker = faker.Faker()
FAKE_TYPES_MAP: dict = {
    str: lambda: FAKE_GEN.pystr(),
    int: lambda: FAKE_GEN.pyint(),  # pylint: disable=W0108
    float: lambda: FAKE_GEN.pyfloat(),  # pylint: disable=W0108
    bool: lambda: random.choice(
        ("1", "yEs", "oK", "True", "On", "oK  ", "false", "False", "NO", "Fake")
    ),  # pylint: disable=W0108
    decimal.Decimal: lambda: FAKE_GEN.pydecimal(),  # pylint: disable=W0108
    pathlib.Path: lambda: pathlib.Path(FAKE_GEN.file_path()),  # pylint: disable=W0108
}


@pytest.mark.parametrize("desired_type", FAKE_TYPES_MAP.keys())
@pytest.mark.parametrize("key_exists", (True, False))
def test_parse_osgetenv_good_and_bad(monkeypatch, desired_type, key_exists) -> None:
    """Test for os.getenv provider.
    """
    env_key: str = f"DEBUGME_KOKOK_PRIVET_{FAKE_GEN.pystr()}"
    original_value: typing.Any = FAKE_TYPES_MAP[desired_type]()
    monkeypatch.setenv(env_key, str(original_value))
    tested_value: typing.Any = envcast.env(env_key if key_exists else FAKE_GEN.pystr(), type_cast=desired_type)
    if key_exists:
        if desired_type == bool:
            assert tested_value == bool(original_value.lower().strip() in envcast.env.BOOLEAN_VALUES)
        else:
            assert tested_value == original_value
    else:
        assert tested_value is None


@pytest.mark.parametrize("desired_type", FAKE_TYPES_MAP.keys())
@pytest.mark.parametrize("key_exists", (True, False))
def test_parse_dotenv_good_and_bad(monkeypatch, desired_type, key_exists) -> None:
    """Test for os.getenv provider.
    """
    dotenv_fn: envcast.base.DotEnvProcessor = envcast.base.DotEnvProcessor()
    env_key: str = f"TEST_KEY_{FAKE_GEN.pystr()}"
    original_value: typing.Any = FAKE_TYPES_MAP[desired_type]()
    monkeypatch.setattr(
        "pathlib.Path.read_text", mock.Mock(return_value=f" {env_key} =  {original_value}\n" if key_exists else "")
    )
    monkeypatch.setattr("pathlib.Path.exists", lambda x: True)
    monkeypatch.setattr("pathlib.Path.is_file", lambda x: True)
    dotenv_fn.set_dotenv_path(".")
    tested_value: typing.Any = dotenv_fn(env_key, type_cast=desired_type)
    if key_exists:
        if desired_type == bool:
            assert tested_value == bool(original_value.lower().strip() in envcast.dotenv.BOOLEAN_VALUES)
        else:
            assert tested_value == original_value
    else:
        assert tested_value is None
