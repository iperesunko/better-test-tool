import json
import os
import re
from collections import defaultdict

from better_test_tool import utils


class FilesScaner(object):
    def __init__(self, pref='test_', suff='.py'):
        self.pref = pref
        self.suff = suff
        self.files = []

    def scan(self, path):
        """
        Scans the directory and selects files according to the specified criteria
        :param str path: test/unit/test_config.py
        :return float: modification time of folder
        """
        found_files = os.walk(path)
        modification_time = os.stat(path).st_mtime

        for dirpath, _, filenames in found_files:
            for _file in filenames:
                if self.files_filter(_file):
                    self.files.append(os.path.join(dirpath, _file))

        return modification_time

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

    _cache_file = utils.get_cache_filename()

    def __init__(self):
        self.file_scaner = FilesScaner()
        self.file_parser = FilesParser()
        self.test_files_structure = {}

    def parse(self, folder_path):
        """
        Searches for test files and parses them
        :param str folder_path: path to target folder
        :return int: number of found test files
        """
        utils.check_test_folder(folder_path)
        m_time = self.file_scaner.scan(folder_path)

        if not self.file_scaner.files:
            raise utils.BTTError('Nothing to parse - no test files')

        for filepath in self.file_scaner.files:
            self.test_files_structure[filepath] = self.file_parser.parse_file(filepath)

        self.test_files_structure.update({'m_time': m_time, 'test_folder': folder_path})
        self._saves_cache()

        return len(self.file_scaner.files)

    def _saves_cache(self):
        """
        Saves a parsed test structure to a json file
        :return:
        """
        with open(self._cache_file, 'w') as outfile:
            json.dump(self.test_files_structure, outfile)
