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

    def __getattr__(self, item):
        # lazy loading of data from the cache
        if item == '_files_structure':
            if os.path.exists(utils.CACHE_FILENAME):
                with open(utils.CACHE_FILENAME) as file:
                    self._files_structure = json.load(file)
            else:
                color_output.error('Cache file not found. First run the command "btt parse folderpath"\n')
                sys.exit(1)

        return self.__dict__.get(item)

    def _generate_regex(self, simplified_path):
        """
        Generate a regex pattern
        :param str simplified_path: 'unit config_server'
        :return str: a string regex
        """
        splitted = simplified_path.split(' ')
        raw = ''.join(['.*{}.*'.format(word) for word in splitted])
        return raw.replace('.*.*', '.*')

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

    def module_selection(self, modules):
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
            color_output.standard(message + '\n')

            result = self.read_user_answer(modules_number)
            module_path = modules[result - 1]
        elif modules_number == 1:
            module_path = modules[0]
        else:
            color_output.warning('No matches found.\n')
            return False

        return module_path


class BaseLauncher(object):
    command_template = None
    finder = Finder()

    def generate(self, simplified_path):
        """
        Generates a command for execution in a manual mode
        :param str simplified_path:
        :return str: a generated command
        """
        modules = self.finder.finds_modules(simplified_path)
        module_filepath = self.finder.module_selection(modules)

        if module_filepath:
            return self.command_template.format(filepath=module_filepath)


class NoseTestsLauncher(BaseLauncher):
    """
    The class implements an interface for interacting with nosetests to generate commands
    """

    def __init__(self):
        super(NoseTestsLauncher,self).__init__()
        self.command_template = 'nosetests -svv {filepath}'


class PytestLauncher(BaseLauncher):
    """
    The class implements an interface for interacting with pytest to generate commands
    """
    def __init__(self):
        super(PytestLauncher, self).__init__()
        self.command_template = 'pytest {filepath} -v'


class AbstractFabricLauncher(object):
    launchers = {
        'nosetests': NoseTestsLauncher(),
        'pytest': PytestLauncher()}

    def __init__(self, launcher):
        self.launcher = self.launchers.get(launcher)

    def generate(self, simplified_path):
        return self.launcher.generate(simplified_path)
