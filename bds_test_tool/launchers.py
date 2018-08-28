import json
import os
import sys

from bds_test_tool.utils import ColorOutput, cache_file_path, search_statistics

color_output = ColorOutput()


class BaseLauncher(object):
    _cache_file = cache_file_path

    def __init__(self):
        self._files_structure = None

    def _open_cache_file(self):
        if isinstance(self._files_structure, dict):
            return True

        if os.path.exists(self._cache_file):
            with open(self._cache_file) as file:
                self._files_structure = json.load(file)
            return True
        else:
            color_output.error('Cache file not found. First run the command "btt parse folderpath"\n')
            return False

    def _check_compliance(self, file_path, simplified_path):
        """
        Checks the path of the module for matching with the specified names
        :param str file_path: 'file-fixtures/unit/server/test_config_server.py'
        :param simplified_path: 'unit server config_server'
        :return bool: True or False
        """
        for name in simplified_path.split(' '):
            if name not in file_path:
                break
        else:
            return True

        return False

    @search_statistics
    def _find_test_module(self, simplified_path):
        matching = []
        modules = self._files_structure.keys()

        for module in modules:
            if self._check_compliance(module, simplified_path):
                matching.append(module)

        return matching

    def _format_multuple_modules(self, modules):
        return '\n'.join(['{}. {}'.format(index, name) for index, name in enumerate(modules, 1)])

    def _read_user_answer(self, range):
        while True:
            try:
                text = sys.stdin.readline()
            except KeyboardInterrupt:
                return
            else:
                text = text.strip()

                if text.isdigit():
                    digit = int(text)

                    if digit > range:
                        color_output.warning('The answer is out of the acceptable range. Choose another answer.\n')
                    else:
                        return digit
                else:
                    color_output.warning('This is not a digit. Please enter the answer again\n')

    def _module_selection_and_generate_command(self, modules):
        modules_number = len(modules)

        if modules_number > 10:
            color_output.warning('Too many suggestions. Please enter a more specific query\n')
            return False
        elif 1 < modules_number <= 10:
            formatted = self._format_multuple_modules(modules)
            message = 'Several modules were found, select the required one:\n' + formatted
            color_output.info(message + '\n')

            result = self._read_user_answer(modules_number)
            module_path = modules[result - 1]
        elif modules_number == 1:
            module_path = modules[0]
        else:
            color_output.warning('No matches found.\n')
            return False

        return module_path

    def generate_command(self, simplified_path):
        raise NotImplemented

    def run(self, simplified_path):
        raise NotImplemented


class NoseTestsLauncher(BaseLauncher):
    _command = 'nosetests -svv {filepath}\n'

    def generate_command(self, simplified_path):
        if self._open_cache_file():
            modules = self._find_test_module(simplified_path)
            module_filepath = self._module_selection_and_generate_command(modules)

            if module_filepath:
                return self._command.format(filepath=module_filepath)

    def run(self, simplified_path):
        if self._open_cache_file():
            command = self.generate_command(simplified_path)
            if command:
                color_output.succes('Run {}'.format(command))


class AbstractLauncherFactory(object):
    nosetests = NoseTestsLauncher()
