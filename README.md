# swapenv -- a handy-dandy .env file switcher

Use `python setup.py install` to install the tool

Assuming you have a project looking like this:

```
.env
environments/
  local.env
  prod.env
stuff/
  *.*
```

### Find out what environment you're on right now
```
echo "I am currently using $(swapenv)"
```

### List available environments
```
$ swapenv -l
Environments Available:
  - local
  - prod
```

### Switch between envs
```
$ swapenv local
"Environment is already <local>

$ swapenv prod
"Switching .env from <local> to <prod>
```

### Need more help?
```
$ swapenv --help

usage: Swap .env file with one in environments directory, safely and easily.

positional arguments:
  target                Name of environment to swap to

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List available environments
  -f, --force           forcibly switch environment (don't check if saved)
  --init                initialize environment directory
  --current CURRENT     Name of current env file
  --env-directory ENV_DIRECTORY
                        path to directory containing .env files
  --env-example-filename ENV_EXAMPLE_FILENAME
                        path to the .env example file
  -s SAVE_AS, --save-as SAVE_AS
                        save current env as something else

```
