"""All logic lie here.
"""
from __future__ import annotations
import os
import abc
import uuid
import typing
import decimal
import pathlib
import functools

from . import exceptions


class GenericEnvironmentProcessor:
    """Main class for the app.
    """

    BOOLEAN_VALUES: tuple[str] = ("1", "y", "yes", "true", "ok", "on")

    @abc.abstractmethod
    def provide_data(self, var_name: str) -> typing.Any:
        raise NotImplemented

    def cast_value_to_exact_type(self, type_cast: type, value: str) -> typing.Any:
        """Wrapper for type casting.
        """
        if type_cast == bool:
            return value.lower().strip() in self.BOOLEAN_VALUES
        else:
            return type_cast(value)

    def __call__(
        self, var_name: str, default_value: typing.Any = None, type_cast: type = str, list_type_cast: type = str
    ) -> typing.Any:
        """Main function.
        """
        result_value: typing.Any
        try:
            result_value = self.provide_data(var_name)
            if not result_value:
                result_value = default_value
        except TypeError:
            result_value = default_value
        if type_cast in [list, tuple]:
            array_values: list = []
            for one_item in result_value.split("," if "," in result_value else " "):
                array_values.append(self.cast_value_to_exact_type(list_type_cast, one_item))
            return array_values if type_cast == list else tuple(array_values)
        else:
            return self.cast_value_to_exact_type(type_cast, result_value) if result_value else None


class OSGetEnvProcessor(GenericEnvironmentProcessor):
    """Provider realise parsing from os.environ.
    """

    def provide_data(self, var_name: str) -> typing.Any:
        """Os getenv provider.
        """
        return os.getenv(var_name)


class DotEnvProcessor(GenericEnvironmentProcessor):
    """Provider realise parsing from .env file.
    """

    DOTENV_FILE_NAME: str = ".env"
    PATH_FOR_DOTENV: pathlib.Path

    def set_dotenv_path(self, full_path: typing.Union[str, pathlib.Path]) -> DotEnvProcessor:
        """Dotenv path helper.
        """
        self.PATH_FOR_DOTENV = pathlib.Path(full_path).resolve()
        if self.PATH_FOR_DOTENV.is_dir():
            self.PATH_FOR_DOTENV = self.PATH_FOR_DOTENV.joinpath(self.DOTENV_FILE_NAME)
        if not self.PATH_FOR_DOTENV.is_file() or not self.PATH_FOR_DOTENV.exists():
            raise exceptions.IncorrectDotenvPath(str(self.PATH_FOR_DOTENV))
        self.PATH_FOR_DOTENV = pathlib.Path(full_path).resolve()

    @functools.lru_cache(maxsize=None)
    def _load_dotenv_file(self) -> dict:
        """Small helper for dotenv provider.
        """
        data_provider: dict = {}
        try:
            statements: list = self.PATH_FOR_DOTENV.read_text().strip().split("\n")
        except FileNotFoundError as exc:
            raise exceptions.IncorrectDotenvPath(exc)
        for one_row in self.PATH_FOR_DOTENV.read_text().strip().split("\n"):
            if not one_row:
                continue
            exp_parts: list = one_row.split("=")
            if len(exp_parts) != 2:
                raise exceptions.BrokenDotenvStructure(one_row)
            data_provider[exp_parts[0].replace("export", "").strip()] = exp_parts[1]
        return data_provider

    def provide_data(self, var_name: str) -> typing.Any:
        """Fetch value from dotenv file.
        """
        return self._load_dotenv_file().get(var_name)


env: OSGetEnvProcessor = OSGetEnvProcessor()
dotenv: DotEnvProcessor = DotEnvProcessor()
