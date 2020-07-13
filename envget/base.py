"""All logic lie here.
"""
from __future__ import annotations
import os
import uuid
import typing
import decimal
import pathlib
import functools


GenericTypes: typing.Union = typing.Union[str, int, bool, float, decimal.Decimal, pathlib.Path, uuid.UUID]
GenericList: typing.Union = typing.Union[
    GenericTypes, typing.List[GenericTypes], typing.Tuple[GenericTypes], typing.Dict[str, GenericTypes], None
]
CURRENT_DIR: pathlib.Path = pathlib.Path().cwd().resolve()
FETCHERS: dict = {}


def fetcher_os_getenv(var_name: str) -> typing.Optional[str]:
    """Fetch value from environ.
    """
    return os.getenv(var_name)


def fetcher_envfile(var_name: str) -> typing.Optional[str]:
    """Fetch value from environ.
    """
    var_name_l: str = var_name.lower()
    data_provider: dict
    if hasattr(fetcher_envfile, "__cache__"):
        data_provider = fetcher_envfile.__cache__
    else:
        env_file: pathlib.Path = CURRENT_DIR.joinpath(".env")
        statements: list = env_file.read_text().split("\n")
        for one_row in statements:
            exp_parts: list = one_row.split("=")
            data_provider[exp_parts[0].lower().replace("export", "").trim()] = exp_parts[1]
    return data_provider[var_name_l] if var_name_l in data_provider else None


def make_env_parser(type_of_fetcher: str = "env") -> typing.Callable:
    """Create env parser instance.
    """
    return functools.partial(parse_env, env_fetcher=FETCHERS[type_of_fetcher])


def caster_for_type(type_cast: type, value: str) -> typing.Optional[GenericTypes]:
    """Wrapper for type casting.
    """
    if type_cast == bool:
        if value.lower() in ("1", "yes", "true", "ok"):
            return True
        else:
            return False
    else:
        return type_cast(value)


def parse_env(
    var_name: str,
    default_value: GenericTypes = "",
    type_cast: type = str,
    list_type_cast: type = str,
    env_fetcher: typing.Callable = lambda: None,
) -> GenericList:
    """Main function.
    """
    result_value: typing.Optional[GenericTypes]
    try:
        result_value = env_fetcher(var_name)
        if not result_value:
            result_value = default_value
    except TypeError:
        result_value = default_value
    if type_cast in [list, tuple]:
        array_values: list = []
        for one_item in result_value.split("," if "," in result_value else " "):
            array_values.append(caster_for_type(list_type_cast, one_item))
        return array_values
    else:
        return caster_for_type(type_cast, result_value) if result_value else None


FETCHERS = {
    "env": fetcher_os_getenv,
    "osenv": fetcher_os_getenv,
    "envfile": fetcher_envfile,
}
env: typing.Callable = make_env_parser("osenv")
envfile: typing.Callable = make_env_parser("envfile")
