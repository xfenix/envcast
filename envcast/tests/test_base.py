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
import envcast.exceptions


FAKE_GEN: faker.Faker = faker.Faker()
FAKE_TYPES_MAP: dict = {
    str: lambda: FAKE_GEN.pystr(),  # pylint: disable=W0108
    int: lambda: FAKE_GEN.pyint(),  # pylint: disable=W0108
    float: lambda: FAKE_GEN.pyfloat(),  # pylint: disable=W0108
    bool: lambda: random.choice(envcast.env.BOOLEAN_VALUES),  # pylint: disable=W0108
    decimal.Decimal: lambda: FAKE_GEN.pydecimal(),  # pylint: disable=W0108
    pathlib.Path: lambda: pathlib.Path(FAKE_GEN.file_path()),  # pylint: disable=W0108
}


def generic_assert(tested_value, original_value, key_exists, desired_type):
    """Generic assert fn.
    """
    if key_exists:
        if desired_type == bool:
            assert tested_value == bool(original_value.lower().strip() in envcast.env.BOOLEAN_VALUES)
        else:
            assert tested_value == original_value
    else:
        assert tested_value is None


@pytest.mark.parametrize("desired_type", FAKE_TYPES_MAP.keys())
@pytest.mark.parametrize("key_exists", (True, False))
def test_parse_osgetenv_good_and_bad(monkeypatch, desired_type, key_exists) -> None:
    """Test for os.getenv provider.
    """
    env_key: str = f"DEBUGME_KOKOK_PRIVET_{FAKE_GEN.pystr()}"
    original_value: typing.Any = FAKE_TYPES_MAP[desired_type]()
    monkeypatch.setenv(env_key, str(original_value))
    generic_assert(
        envcast.env(env_key if key_exists else FAKE_GEN.pystr(), type_cast=desired_type),
        original_value,
        key_exists,
        desired_type,
    )


@pytest.mark.parametrize("desired_type", FAKE_TYPES_MAP.keys())
@pytest.mark.parametrize("key_exists", (True, False))
@pytest.mark.parametrize("broken_equal_sign", (True, False))
def test_parse_dotenv_good_and_bad(monkeypatch, desired_type, key_exists, broken_equal_sign) -> None:
    """Test for .env provider.
    """
    dotenv_fn: envcast.base.DotEnvProcessor = envcast.base.DotEnvProcessor()
    env_key: str = f"TEST_KEY_{FAKE_GEN.pystr()}"
    original_value: typing.Any = FAKE_TYPES_MAP[desired_type]()
    var_separator: str = "HAHA_DEBUGME-fail:(" if broken_equal_sign else "="
    monkeypatch.setattr(
        "pathlib.Path.read_text",
        mock.Mock(return_value=f" {env_key} {var_separator}  {original_value}\n" if key_exists else ""),
    )
    monkeypatch.setattr("pathlib.Path.exists", lambda x: True)
    monkeypatch.setattr("pathlib.Path.is_file", lambda x: True)
    dotenv_fn.set_dotenv_path(".")
    try:
        generic_assert(dotenv_fn(env_key, type_cast=desired_type), original_value, key_exists, desired_type)
    except envcast.exceptions.BrokenDotenvStructure:
        assert broken_equal_sign


@pytest.mark.parametrize("desired_type", (tuple, list))
@pytest.mark.parametrize("desired_sub_type", tuple(FAKE_TYPES_MAP.keys()))
@pytest.mark.parametrize("separator", sorted(tuple(envcast.env.SEPARATORS_FOR_LIST_TYPE)))
def test_list_types(monkeypatch, desired_type, desired_sub_type, separator) -> None:
    """Test with list based variables.
    """
    generated_values: list = desired_type([FAKE_TYPES_MAP[desired_sub_type]() for _ in range(FAKE_GEN.pyint(10, 50))])
    env_key: str = f"HEYPRIVET_KAKDELA_A_{FAKE_GEN.pystr()}"
    monkeypatch.setenv(env_key, separator.join([str(one_item) for one_item in generated_values]))
    tested_value: typing.Any = envcast.env(env_key, type_cast=desired_type, list_type_cast=desired_sub_type)
    if desired_sub_type == bool:
        generated_values = desired_type(
            [bool(one_item.lower().strip() in envcast.env.BOOLEAN_VALUES) for one_item in generated_values]
        )
    assert tested_value == generated_values


def test_abstract_method():
    """We want to test everything, of course.
    """
    with pytest.raises(NotImplementedError):
        envcast.base.GenericEnvironmentProcessor().provide_data("debug")


def test_list_types_with_empty_list(monkeypatch) -> None:
    """Test with list based variables.
    """
    desired_type: type = list
    desired_sub_type: type = int
    generated_values: list = desired_type([FAKE_TYPES_MAP[desired_sub_type]() for _ in range(FAKE_GEN.pyint(10, 50))])
    env_key: str = f"HEYPRIVET_KAKDELA_A_{FAKE_GEN.pystr()}"
    monkeypatch.setenv(env_key, "@".join([str(one_item) for one_item in generated_values]))
    tested_value: typing.Any = envcast.env(env_key, type_cast=desired_type, list_type_cast=desired_sub_type)
    assert tested_value == []


@pytest.mark.parametrize("test_dotenv_path", (".", "/", "nonexistent"))
@pytest.mark.parametrize("fail_method", ("pathlib.Path.exists", "pathlib.Path.is_file"))
def test_parse_dotenv_setdotenv_path_method(monkeypatch, test_dotenv_path, fail_method) -> None:
    """Test exception with bad test env path.
    """
    monkeypatch.setattr(fail_method, lambda x: False)
    with pytest.raises(envcast.exceptions.IncorrectDotenvPath):
        envcast.base.DotEnvProcessor().set_dotenv_path(test_dotenv_path)


def test_parse_dotenv_with_is_a_directory_error(monkeypatch) -> None:
    """Test exception with is a directory fail.
    """
    dotenv_fn: envcast.base.DotEnvProcessor = envcast.base.DotEnvProcessor()
    monkeypatch.setattr("pathlib.Path.exists", lambda x: True)
    monkeypatch.setattr("pathlib.Path.is_file", lambda x: True)
    monkeypatch.setattr("pathlib.Path.read_text", mock.Mock(side_effect=IsADirectoryError))
    dotenv_fn.set_dotenv_path(".")
    with pytest.raises(envcast.exceptions.IncorrectDotenvPath):
        dotenv_fn("hahah")
