import argparse
import os
from collections import OrderedDict

import sys

from swapenv import DEFAULT_ENV_DIRECTORY, DEFAULT_ENV_EXAMPLE_FILENAME

_options = {
    '-l/--list': {
        'help': 'List available environments',
        'action': 'store_true'
    },
    '-f/--force': {
        'help': "forcibly switch environment (don't check if saved)",
        'action': 'store_true'
    },
    '--init': {
        'help': 'initialize environment directory',
        'action': 'store_true'
    },
    '--current': {
        'help': 'Name of current env file',
        'default': '.env'
    },
    '--env-directory': {
        'help': 'path to directory containing .env files',
        'default': DEFAULT_ENV_DIRECTORY
    },
    '--env-example-filename': {
        'help': 'path to the .env example file',
        'default': DEFAULT_ENV_EXAMPLE_FILENAME
    },
    '-s/--save-as': {
        'help': 'save current env as something else',
        'type': str,
        'default': None
    },
    'target': {
        'help': 'Name of environment to swap to',
        'default': None,
        'nargs': '?'
    },
}


def build_parser(options: dict = _options) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser('swapenv', 'Swap .env file with one in environments directory, safely and easily.')

    for name, kwargs in options.items():
        parser.add_argument(*name.split('/'), **kwargs)
    return parser


class CliArgumentError(Exception):
    pass


class CliArguments(object):
    def __init__(self, args):
        self.target = args.target  # type: str
        self.active_env_filename = args.current  # type: str
        self.force = args.force  # type: bool
        self.list = args.list # type: bool
        self.init = args.init  # type: bool
        self.save_as = args.save_as  # type: str
        self.env_directory = args.env_directory  # type: str
        self.use_cwd = not os.path.isabs(args.env_directory)  # type: bool
        self.env_example_filename = args.env_example_filename  # type: str


def run(args: CliArguments):
    from swapenv.core import Swapper
    swapper = Swapper(args)

    env_files = swapper.env_files

    if args.list:
        list_env_files(env_files)
        return 0

    existing_env_name = swapper.existing_env_name

    if args.target is None:
        sys.stdout.write(existing_env_name or 'NONE')
        return 0

    if existing_env_name == args.target:
        print(f"Environment is already <{existing_env_name}>")
        return 0

    return swapper.swap(force=args.force, save_as=args.save_as)


def list_env_files(env_files: OrderedDict):
    print('Environments Available:')
    for k in env_files:
        print(f"  - {k}")


def main(args: list = None):
    parser = build_parser(_options)
    arguments = parser.parse_args(args=args)

    run(CliArguments(arguments))


if __name__ == '__main__':
    main()
