envcast
===
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Python package for environment parsing + type casting. Why do you need it? Because you cand just grab environment variables as is, you need to cast them to desired types for your application (for exmplae like bool variable: how to cast strings False, "", 0 to bool without boilerplaite?).  
This packages just cast needed environment variables to desired types.

Written in modern python 3.7+ with full support of:
* https://www.python.org/dev/peps/pep-0526/
* https://www.python.org/dev/peps/pep-0484/
* https://www.python.org/dev/peps/pep-0008/
* https://www.python.org/dev/peps/pep-0257/
* https://www.python.org/dev/peps/pep-0518/
* https://www.python.org/dev/peps/pep-0585/


Usage examples
===

### API
Signature of env and dotenv absolutely similar and looks like this:
```python
# LISTING_CASTING_FN applies if CASTING_FN is list, tuple
# default_value going through type casting, so it must be in desired type
# default value for CASTING_FN is str
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
