import json
import os
import re
import sys

from better_test_tool import utils

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

    def find_tests(self, module_path, simplified_path):
        """
        Finds a test case from module
        :param str module_path: '/tests/unit/config_server.py'
        :param str simplified_path: 'connect config server'
        :return list: list of matched tests
        """
        matching = []
        regex = self._generate_regex(simplified_path)
        module_dict = self._files_structure.get(module_path)

        for parent in module_dict.keys():
            for test in module_dict[parent]:
                if re.match(regex, test):
                    matching.append('{} {}'.format(parent, test))

        return matching

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

    def item_selection(self, items, target='modules'):
        """
        Displays the list of modules on the screen. If more than 10 options -
        asks the user to select the desired one
        :param list items: list of modules paths
        :param str target: 'modules' or 'test cases'
        :return str: module that the user selected
        """
        modules_number = len(items)

        if modules_number > 10:
            color_output.warning('Too many suggestions. Please enter a more specific query\n')
            return False
        elif 1 < modules_number <= 10:
            formatted = utils.format_multuple_modules(items)
            message = 'Several {} were found, select the required one:\n'.format(target) + formatted
            color_output.standard(message + '\n')

            result = self.read_user_answer(modules_number)
            module_path = items[result - 1]
        elif modules_number == 1:
            module_path = items[0]
        else:
            color_output.warning('No matches found.\n')
            return False

        return module_path


class BaseLauncher(object):
    raw_function = re.compile(r'^functions\s')
    command_template = None
    module_separator = None
    test_case_separator = None
    finder = Finder()

    def generate(self, module_path, method=None):
        """
        Generates a command for execution in a manual mode
        :param str module_path:
        :param str method:
        :return str: a generated command
        """
        target = None
        modules = self.finder.finds_modules(module_path)
        module_filepath = self.finder.item_selection(modules)

        if method and module_filepath:
            test_cases = self.finder.find_tests(module_filepath, method)
            test_case = self.finder.item_selection(test_cases, target='test cases')
            if test_case:
                target = self.target_formation(module_filepath, test_case)

        elif module_filepath:
            target = module_filepath

        if target:
            return self.command_template.format(target=target)

        return

    def cleanup(self, method):
        return self.raw_function.sub('', method)

    def target_formation(self, module_path, method):
        """
        Generates a target (test case) path for running by launchers
        :param str module_path:
        :param str method:
        :return str:
        """
        test_case = self.cleanup(method)
        test = self.test_case_separator.join(test_case.split())
        return '{}{}{}'.format(module_path, self.module_separator, test)


class NoseTestsLauncher(BaseLauncher):
    """
    The class implements an interface for interacting with nosetests to generate commands
    """

    def __init__(self):
        super(NoseTestsLauncher, self).__init__()
        self.command_template = 'nosetests -svv {target}'
        self.module_separator = ':'
        self.test_case_separator = '.'


class PytestLauncher(BaseLauncher):
    """
    The class implements an interface for interacting with pytest to generate commands
    """

    def __init__(self):
        super(PytestLauncher, self).__init__()
        self.command_template = 'pytest {target} -v'
        self.module_separator = '::'
        self.test_case_separator = '::'
