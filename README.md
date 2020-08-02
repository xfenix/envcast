envcast
===
![Build and publish](https://github.com/xfenix/envcast/workflows/Build%20and%20publish/badge.svg)
[![PyPI version](https://badge.fury.io/py/envcast.svg)](https://badge.fury.io/py/envcast)
[![codecov](https://codecov.io/gh/xfenix/envcast/branch/master/graph/badge.svg)](https://codecov.io/gh/xfenix/envcast)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Imports: isort](https://img.shields.io/badge/imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)

Python package for environment parsing + type casting. Why do you need it? Because you can't just grab environment variables as is, you need to cast them to desired types for your application (for example like bool variable: how to cast strings `False`, `""`, `0` to bool without boilerplaite?).  
This packages just cast needed environment variables to desired types with syntax very familiar to `os.getenv` users.  
Plus this package has good test coverage and quality codebase.  
Written in modern python 3.7+ with full support of:
* https://www.python.org/dev/peps/pep-0526/
* https://www.python.org/dev/peps/pep-0484/
* https://www.python.org/dev/peps/pep-0008/
* https://www.python.org/dev/peps/pep-0257/
* https://www.python.org/dev/peps/pep-0518/
* https://www.python.org/dev/peps/pep-0585/


Usage
===
### API
Signature of env and dotenv absolutely similar and looks like this:
```python
# var_name is desired variable name
# default_value going through type casting, so it must be in desired type
# type_cast — desired variable type casting function
# list_type_cast applies if type_cast is list, tuple
envcast.env(var_name: str, default_value: typing.Any = None, type_cast: type = str, list_type_cast: type = str)
```

### From environment variables
For casting good old plain env variables you will need do following:
```python
import envcast


this_will_be_bool: bool = envcast.env('SOME_ENV_VARIABLE', 'false', type_cast=bool))
or_this_is_string_by_default: str = envcast.env('OTHER_ENV_VAR')
this_is_int: int = envcast.env('MORE_ENV', type_cast=int)
```

### From .env file
If your are using .env file, you can do it too:
```python
import envcast


envcast.set_dotenv_path('.')
# Can be any of the following :
# envcast.set_dotenv_path('~/some/.env')
# envcast.set_dotenv_path('/tmp/.env')
# envcast.set_dotenv_path('/tmp/')
this_will_be_bool: bool = envcast.dotenv('SOME_ENV_VARIABLE', 'false', type_cast=bool))
or_this_is_string_by_default: str = envcast.dotenv('OTHER_ENV_VAR')
this_is_int: int = envcast.dotenv('MORE_ENV', type_cast=int)
```
Dont worry, file will be readed and parsed only once.


### Exceptions
* envcast.exceptions.IncorrectDotenvPath
* envcast.exceptions.NotSettedDotenvPath
* envcast.exceptions.BrokenDotenvStructure


### Supported casting types
You can pass to `type_cast` or `list_type_cast` any desired type casting callables.
It may be any builtin type, of Decimal, Path, or any other callable.


### Listing values
If you want to parse and cast environment variable with list of values:
```
MY_FANCY_VAR=True, On, Ok, False, Disabled, 0
```
You will need expression like this:
```
envcast.env('MY_FANCY_VAR', type_cast=bool, list_type_cast=list)
```
If you cares about what exactly can be separator for list values: it can be `,` or ` ` (space).


Changelog
===
You can check https://github.com/xfenix/envcast/releases/ release page.
