"""All logic lie here.
"""
from __future__ import annotations
import os
import abc
import typing
import logging
import pathlib
import functools

from . import exceptions


LOGGER_OBJ: logging.Logger = logging.getLogger(__file__)


class GenericEnvironmentProcessor:
    """Main class for the app.
    """

    BOOLEAN_VALUES: tuple[str] = ("1", "y", "yes", "true", "ok", "okay", "on", "enabled")
    SEPARATORS_FOR_LIST_TYPE: set[str] = {"|", ",", " "}

    @abc.abstractmethod
    def provide_data(self, var_name: str) -> typing.Any:
        """Provide data method. Override it in children.
        """
        raise NotImplementedError

    def cast_value_to_exact_type(self, type_cast: type, value: str) -> typing.Any:
        """Wrapper for type casting.
        """
        if type_cast == bool:
            return value.lower().strip() in self.BOOLEAN_VALUES
        return type_cast(value)

    def __call__(
        self, var_name: str, default_value: typing.Any = None, type_cast: type = str, list_type_cast: type = str
    ) -> typing.Any:
        """Main function.
        """
        # prepared result value
        prepared_value: typing.Any = self.provide_data(var_name)
        if not prepared_value:
            prepared_value = default_value
        # if already in desired type — return as is
        if isinstance(prepared_value, type_cast):
            return prepared_value
        if not prepared_value:
            return None
        # list casting
        if type_cast in {list, tuple}:
            output_values: list = []
            prepared_list: list = []
            for one_separator in self.SEPARATORS_FOR_LIST_TYPE:
                if one_separator in prepared_value:
                    prepared_list = prepared_value.split(one_separator)
                    break
            if not prepared_list:
                LOGGER_OBJ.info(f"Separator for {var_name} is not found. Trying to parse value: {prepared_value}")
            for one_item in prepared_list:
                output_values.append(self.cast_value_to_exact_type(list_type_cast, one_item))
            return type_cast(output_values)
        # plain basic casting
        return self.cast_value_to_exact_type(type_cast, prepared_value)


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
    path_for_dotenv: pathlib.Path

    def set_dotenv_path(self, full_path: typing.Union[str, pathlib.Path]) -> DotEnvProcessor:
        """Dotenv path helper.
        """
        self.path_for_dotenv = pathlib.Path(full_path).resolve()
        if self.path_for_dotenv.is_dir():
            self.path_for_dotenv = self.path_for_dotenv.joinpath(self.DOTENV_FILE_NAME)
        if not self.path_for_dotenv.is_file() or not self.path_for_dotenv.exists():
            raise exceptions.IncorrectDotenvPath(str(self.path_for_dotenv))
        self.path_for_dotenv = pathlib.Path(full_path).resolve()

    @functools.lru_cache(maxsize=None)
    def _load_dotenv_file(self) -> dict:
        """Small helper for dotenv provider.
        """
        data_provider: dict = {}
        try:
            statements: list = self.path_for_dotenv.read_text().strip().split("\n")
        except IsADirectoryError as exc:
            raise exceptions.IncorrectDotenvPath(exc)
        for one_row in statements:
            if not one_row:
                continue
            exp_parts: list = one_row.split("=")
            if len(exp_parts) != 2:
                raise exceptions.BrokenDotenvStructure(one_row)
            data_provider[exp_parts[0].replace("export", "").strip()] = exp_parts[1].strip()
        return data_provider

    def provide_data(self, var_name: str) -> typing.Any:
        """Fetch value from dotenv file.
        """
        return self._load_dotenv_file().get(var_name)


env: OSGetEnvProcessor = OSGetEnvProcessor()
dotenv: DotEnvProcessor = DotEnvProcessor()
