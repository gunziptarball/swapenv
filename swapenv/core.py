#!/usr/bin/env python
import functools
import os
import typing
from collections import OrderedDict

from swapenv.cli import CliArguments


class Swapper(object):
    def __init__(self, args: CliArguments = None, **kwargs):
        self.__active_env_filename = None
        self.__existing_env_name = None

        self._env_files = None
        self._environments = None

        env_directory = args.env_directory or kwargs.get('env_directory')
        init = args.init or kwargs.get('init')
        active_env_filename = args.active_env_filename or kwargs.get('active_env_filename')
        env_example_filename = args.env_example_filename or kwargs.get('env_example_filename')
        target = args.target or kwargs.get('target')

        if not os.path.isabs(env_directory):
            env_directory = os.path.join(os.curdir, env_directory)
        if not (os.path.exists(env_directory)):
            if not init:
                raise FileNotFoundError(f'directory {env_directory} does not exist!. '
                                        f'please create, or pass --init flag to swapenv')
            else:
                os.mkdir(env_directory)

        if not os.path.isabs(env_example_filename):
            env_example_filename = os.path.join(os.path.curdir, env_example_filename)
        if not os.path.isabs(active_env_filename):
            active_env_filename = os.path.join(os.path.curdir, active_env_filename)

        self.env_example_filename = env_example_filename

        self.env_directory = env_directory
        self.active_env_filename = active_env_filename
        self.target = target

    @property
    def active_env_filename(self):
        return os.path.normpath(self.__active_env_filename)

    @active_env_filename.setter
    def active_env_filename(self, active_env_filename):
        self._ensure_active_env_file(active_env_filename, self.env_example_filename)
        self.__active_env_filename = active_env_filename

    @property
    @functools.lru_cache(1)
    def env_files(self) -> OrderedDict:
        return self.__open_env_files()

    @property
    def existing_env_name(self) -> str:
        existing_name = self.__existing_env_name
        if existing_name is None:
            existing_name = self.__existing_env_name = self._find_matching_env_by_content(self.read_text_from_current())
        return existing_name

    @existing_env_name.setter
    def existing_env_name(self, val: str):
        self.__existing_env_name = val

    @functools.lru_cache(1)
    def read_text_from_current(self) -> str:
        with open(self.active_env_filename) as f:
            current_env_text = f.read().strip()
        return current_env_text

    def swap(self, force=False, save_as=None):
        if self.existing_env_name is None:
            self.existing_env_name = self._handle_unsaved(force, save_as)

        print(f"Swapping {self.active_env_filename} from <{self.existing_env_name}> to <{self.target}>")
        with open(self.active_env_filename, 'w') as fout:
            fout.write(self.env_files[self.target].strip())
        return 0

    def _find_matching_env_by_content(self, env_text) -> typing.Optional[str]:
        items = self.env_files.items()
        for name, comp in items:
            if comp.strip() == env_text.strip():
                return name
        return None

    @staticmethod
    def _ensure_active_env_file(active_env_filename, env_example_filename):
        if not os.path.exists(active_env_filename):
            if os.path.exists(env_example_filename):
                with open(env_example_filename) as fin:
                    with open(active_env_filename, 'w') as fout:
                        fout.write(fin.read())
            else:
                current_env_text = '# new environment'
                with open('.env', 'w') as f:
                    f.write(current_env_text)

    def __open_env_files(self):
        envs = OrderedDict()
        for name, ext in [os.path.splitext(f) for f in os.listdir(self.env_directory)]:
            if ext == '.env':
                with open(self._get_env_file_path(name)) as f:
                    envs[name] = f.read()
        return envs

    def _get_env_file_path(self, name):
        n, e = os.path.splitext(name)
        if e == '.env':
            name = n
        return os.path.normpath(os.path.join(self.env_directory, name + '.env'))

    def _handle_unsaved(self, force: bool, save_as: typing.Optional[str]):
        if save_as is not None:
            with open(os.path.join(self.env_directory, f'{save_as}.env'), 'w') as f:
                f.write(self.read_text_from_current())
            self.existing_env_name = save_as
        else:
            if not force:
                raise FileNotFoundError(f'Environment {self.existing_env_name} has not been saved.')
        return self.existing_env_name
