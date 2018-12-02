import json
import os
import re
from collections import defaultdict

from better_test_tool import utils

color_output = utils.ColorOutput()


class FilesScaner(object):
    def __init__(self, pref='test_', suff='.py'):
        self.pref = pref
        self.suff = suff
        self.files = []

    def scan(self, path):
        """
        Scans the directory and selects files according to the specified criteria
        :param str path: test/unit/test_config.py
        :return:
        """
        found_files = os.walk(path)

        for dirpath, _, filenames in found_files:
            for _file in filenames:
                if self.files_filter(_file):
                    self.files.append(os.path.join(dirpath, _file))

    def files_filter(self, file):
        """
        Filter files according to the specified criteria
        :param str file: a filename
        :return bool:
        """
        if file.startswith(self.pref) and file.endswith(self.suff):
            return True

        return False


class FilesParser(object):
    re_class = re.compile(r'^class (\w+)')
    re_method = re.compile(r'^\s{4}def (\w+)\(self')
    re_function = re.compile(r'^def (\w+)')

    def parse_file(self, path):
        """
        Parses the input file. Lookup for class, method, and function names
        :param str path: test/unit/test_config.py
        :return dict: key - filepath, value dict with parsed structure
        """
        metadata = defaultdict(list)
        with open(path) as _file:
            text = _file.readlines()

        current_class = None
        for line in text:
            _class = self.re_class.match(line)
            _method = self.re_method.match(line)
            _function = self.re_function.match(line)

            if _class:
                current_class = _class.groups()[0]

            if _method:
                method = _method.groups()[0]
                if method.startswith('test_'):
                    metadata[current_class].append(method)
            elif _function:
                func = _function.groups()[0]
                if func.startswith('test_'):
                    metadata['functions'].append(func)

        return metadata


class ParserTests:
    """
    The class contains commands for parsing the structure of tests,
    saving to the cache and displaying it on the screen
    """

    _cache_file = utils.CACHE_FILENAME

    def __init__(self):
        self.file_scaner = FilesScaner()
        self.file_parser = FilesParser()
        self._test_files_structure = {}

    def parse(self, folder_path, without_caching=False):
        """
        Searches for test files and parses them
        :param str folder_path: path to target folder
        :param bool without_caching:
        """
        self.file_scaner.scan(folder_path)

        if not self.file_scaner.files:
            color_output.warning('Nothing to parse - no test files\n')
            return

        for filepath in self.file_scaner.files:
            self._test_files_structure[filepath] = self.file_parser.parse_file(filepath)

        color_output.succes('Parsing completed. Found {} files.\n'.format(len(self.file_scaner.files)))

        if not without_caching:
            self._saves_cache()

    def show_test_structure(self):
        """
        Displays a list of parsed files or an error message
        :return:
        """
        if os.path.exists(self._cache_file):
            with open(self._cache_file) as file:
                data = json.load(file)

            files = data.keys()
            formatted = utils.format_multuple_modules(files) + '\n'
            color_output.info(formatted)
        else:
            color_output.warning('Nothing to show. Before call this command run the "parse" command\n')

    def _saves_cache(self):
        """
        Saves a parsed test structure to a json file
        :return:
        """
        with open(self._cache_file, 'w') as outfile:
            json.dump(self._test_files_structure, outfile)
