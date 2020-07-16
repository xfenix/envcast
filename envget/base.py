"""All logic lie here.
"""
from __future__ import annotations
import os
import uuid
import typing
import decimal
import pathlib
import functools

from . import exceptions


DOTENV_FILE_NAME: str = ".env"
DOTENV_PATH: pathlib.Path
BOOLEAN_VALUES: tuple[str] = ("1", "y", "yes", "true", "ok", "on")


def set_dotenv_path(full_path: typing.Union[str, pathlib.Path]) -> None:
    """Dotenv path helper.
    """
    DOTENV_PATH = pathlib.Path(full_path).resolve()
    if DOTENV_PATH.is_dir():
        DOTENV_PATH = DOTENV_PATH.joinpath(DOTENV_FILE_NAME)
    if not DOTENV_PATH.is_file() or not DOTENV_PATH.exists():
        raise exceptions.IncorrectDotenvPath(str(DOTENV_PATH))


def getenv_provider(var_name: str) -> typing.Any:
    """Fetch value from environ.
    """
    return os.getenv(var_name)


def dotenv_provider(var_name: str) -> typing.Any:
    """Fetch value from environ.
    """
    data_provider: dict
    if hasattr(dotenv_provider, "__cache__"):
        data_provider = dotenv_provider.__cache__
    else:
        data_provider = {}
        try:
            statements: list = DOTENV_PATH.read_text().strip().split("\n")
        except NameError:
            raise exceptions.NotSettedDotenvPath(DOTENV_PATH)
        for one_row in statements:
            if not one_row:
                continue
            exp_parts: list = one_row.split("=")
            data_provider[exp_parts[0].lower().replace("export", "").strip()] = exp_parts[1]
        dotenv_provider.__cache__ = data_provider
    return data_provider.get(var_name)


def make_env_parser(fetcher_fn: typing.Callable) -> typing.Callable:
    """Create env parser instance.
    """
    return functools.partial(parse_and_cast_var, fetch_value_from_env=fetcher_fn)


def cast_value_to_exact_type(type_cast: type, value: str) -> typing.Any:
    """Wrapper for type casting.
    """
    if type_cast == bool:
        return value.lower() in BOOLEAN_VALUES
    else:
        return type_cast(value)


def parse_and_cast_var(
    var_name: str,
    default_value: typing.Any = "",
    type_cast: type = str,
    list_type_cast: type = str,
    fetch_value_from_env: typing.Callable = lambda: None,
) -> typing.Any:
    """Main function.
    """
    result_value: typing.Any
    try:
        result_value = fetch_value_from_env(var_name.lower().strip())
        breakpoint()
        if not result_value:
            result_value = default_value
    except TypeError:
        result_value = default_value
    if type_cast in [list, tuple]:
        array_values: list = []
        for one_item in result_value.split("," if "," in result_value else " "):
            array_values.append(cast_value_to_exact_type(list_type_cast, one_item))
        return array_values
    else:
        return cast_value_to_exact_type(type_cast, result_value) if result_value else None


env: typing.Callable = make_env_parser(getenv_provider)
dotenv: typing.Callable = make_env_parser(dotenv_provider)
