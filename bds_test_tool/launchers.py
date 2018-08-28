import json
import os
import re
import sys

from bds_test_tool import utils

color_output = utils.ColorOutput()


class Finder(object):
    """
    The class searches for the corresponding modules, generates a list of options
    """
    _cache_file = utils.CACHE_FILE_PATH

    def __init__(self):
        self._files_structure = None

    def open_cache_file(self):
        """
        Loads a cache file if is exists or return an error message
        :return bool:
        """
        if isinstance(self._files_structure, dict):
            return True

        if os.path.exists(self._cache_file):
            with open(self._cache_file) as file:
                self._files_structure = json.load(file)
            return True

        color_output.error('Cache file not found. First run the command "btt parse folderpath"\n')
        return False

    def _generate_regex(self, simplified_path):
        """
        Generate a regex pattern
        :param str simplified_path: 'unit config_server'
        :return str: a string regex
        """
        splitted = simplified_path.split(' ')
        raw = ''.join(['.*{}.*'.format(word) for word in splitted])
        return raw.replace('.*.*', '.*')

    @utils.search_statistics
    def finds_modules(self, simplified_path):
        """
        Finds modules that matched by regex pattern
        :param str simplified_path: 'func server'
        :return list: list of matched modules
        """
        matching = []
        modules = self._files_structure.keys()
        regex = self._generate_regex(simplified_path)

        for module in modules:
            if re.match(regex, module):
                matching.append(module)

        return matching

    def find(self, simplified_path):
        """
        Shows all files that matched by pattern
        :param str simplified_path: config_server
        :return:
        """
        self.open_cache_file()
        modules = self.finds_modules(simplified_path)

        if not modules:
            color_output.warning('No matches found.\n')
        else:
            formatted = utils.format_multuple_modules(modules) + '\n'
            color_output.info(formatted)

    def read_user_answer(self, _range):
        """
        With several options - asks the user to select the desired option
        :param int _range: number of options
        :return int: number
        """
        while True:
            try:
                text = sys.stdin.readline()
            except KeyboardInterrupt:
                return
            else:
                text = text.strip()

                if text.isdigit():
                    digit = int(text)

                    if digit > _range:
                        color_output.warning('The answer is out of the acceptable range. Choose another answer.\n')
                    else:
                        return digit
                else:
                    color_output.warning('This is not a digit. Please enter the answer again\n')

    def module_selection_and_generate_command(self, modules):
        """
        Displays the list of modules on the screen. If more than 10 options -
        asks the user to select the desired one
        :param list modules: list of modules paths
        :return str: module that the user selected
        """
        modules_number = len(modules)

        if modules_number > 10:
            color_output.warning('Too many suggestions. Please enter a more specific query\n')
            return False
        elif 1 < modules_number <= 10:
            formatted = utils.format_multuple_modules(modules)
            message = 'Several modules were found, select the required one:\n' + formatted
            color_output.info(message + '\n')

            result = self.read_user_answer(modules_number)
            module_path = modules[result - 1]
        elif modules_number == 1:
            module_path = modules[0]
        else:
            color_output.warning('No matches found.\n')
            return False

        return module_path


class NoseTestsLauncher(object):
    """
    The class implements an interface for interacting with nosetests to generate and run commands
    """
    command_template = 'nosetests -svv {filepath}\n'
    finder = Finder()

    def generate(self, simplified_path):
        """
        Generates a command for execution in a manual mode
        :param str simplified_path:
        :return str: a generated command
        """
        if self.finder.open_cache_file():
            modules = self.finder.finds_modules(simplified_path)
            module_filepath = self.finder.module_selection_and_generate_command(modules)

            if module_filepath:
                return self.command_template.format(filepath=module_filepath)

    def run(self, simplified_path):
        """
        Executes the generated command
        :param str simplified_path:
        :return:
        """
        if self.finder.open_cache_file():
            command = self.generate(simplified_path)
            if command:
                color_output.succes('Run {}'.format(command))
