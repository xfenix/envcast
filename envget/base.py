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


class EnvParserWrapper:
    """
    """

    DOTENV_FILE_NAME: str = ".env"
    BOOLEAN_VALUES: tuple[str] = ("1", "y", "yes", "true", "ok", "on")

    def __init__(self):
        self.DATA_PROVIDERS: dict[str, typing.Callable] = {
            "env": os.getenv,
            "dotenv": self.dotenv_provider,
        }

    def set_data_provider(self, provider_type: str) -> None:
        """Set data provider.
        """
        self._current_provider: typing.Callable = self.DATA_PROVIDERS[provider_type]
        return self

    def set_dotenv_path(self, full_path: typing.Union[str, pathlib.Path]) -> None:
        """Dotenv path helper.
        """
        DOTENV_PATH = pathlib.Path(full_path).resolve()
        if DOTENV_PATH.is_dir():
            DOTENV_PATH = DOTENV_PATH.joinpath(self.DOTENV_FILE_NAME)
        if not DOTENV_PATH.is_file() or not DOTENV_PATH.exists():
            raise exceptions.IncorrectDotenvPath(str(DOTENV_PATH))
        DOTENV_PATH = pathlib.Path(full_path).resolve()

    def dotenv_provider(self, var_name: str) -> typing.Any:
        """Fetch value from environ.
        """
        data_provider: dict
        if hasattr(self, "__cache__"):
            data_provider = self.__cache__
        else:
            data_provider = {}
            try:
                statements: list = DOTENV_PATH.read_text().strip().split("\n")
            except NameError:
                raise exceptions.NotSettedDotenvPath()
            for one_row in statements:
                if not one_row:
                    continue
                exp_parts: list = one_row.split("=")
                data_provider[exp_parts[0].lower().replace("export", "").strip()] = exp_parts[1]
            self.__cache__ = data_provider
        return data_provider.get(var_name)

    def cast_value_to_exact_type(self, type_cast: type, value: str) -> typing.Any:
        """Wrapper for type casting.
        """
        if type_cast == bool:
            return value.lower().strip() in BOOLEAN_VALUES
        else:
            return type_cast(value)

    def __call__(
        self, var_name: str, default_value: typing.Any = "", type_cast: type = str, list_type_cast: type = str
    ) -> typing.Any:
        """Main function.
        """
        result_value: typing.Any
        try:
            result_value = self._current_provider(var_name)
            if not result_value:
                result_value = default_value
        except TypeError:
            result_value = default_value
        if type_cast in [list, tuple]:
            array_values: list = []
            for one_item in result_value.split("," if "," in result_value else " "):
                array_values.append(self.cast_value_to_exact_type(list_type_cast, one_item))
            return array_values
        else:
            return self.cast_value_to_exact_type(type_cast, result_value) if result_value else None


env: typing.Callable = EnvParserWrapper().set_data_provider("env")
dotenv: typing.Callable = EnvParserWrapper().set_data_provider("dotenv")
