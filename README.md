# Envget
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
For casting good old plain env variables you will need do following:
```python
import envget


this_will_be_bool: bool = envget.env('SOME_ENV_VARIABLE', 'false', cast=bool))
or_this_is_string_by_default: str = envget.env('OTHER_ENV_VAR')
this_is_int: int = envget.env('MORE_ENV', cast=int)
```


If your are using .env file, you can do it too:
```python
import envget


this_will_be_bool: bool = envget.dotenv('SOME_ENV_VARIABLE', 'false', cast=bool))
or_this_is_string_by_default: str = envget.dotenv('OTHER_ENV_VAR')
this_is_int: int = envget.dotenv('MORE_ENV', cast=int)
```
Dont worry, file readed and parsed only once.
