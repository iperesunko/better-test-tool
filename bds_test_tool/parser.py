import json
import os
import re
import sys
from collections import defaultdict
from pprint import pprint
from bds_test_tool.utils import ColorOutput

color_output = ColorOutput()
work_directory = os.path.dirname(os.path.realpath(__file__))


class FilesScaner:
    files = []

    def __init__(self, pref, suff):
        self.pref = pref
        self.suff = suff

    def _scan(self, path):
        found_files = os.walk(path)

        for dirpath, _, filenames in found_files:
            for _file in filenames:
                if self._files_filter(_file):
                    self.files.append(os.path.join(dirpath, _file))

    def _files_filter(self, file):
        if file.startswith(self.pref) and file.endswith(self.suff):
            return True

        return False

    def _show_files(self):
        pprint(self.files)


class FilesParser:
    re_class = re.compile(r'class (\w+)')
    re_method = re.compile(r'\s+def (\w+)')
    re_function = re.compile(r'def (\w+)')

    def _parse_file(self, path):
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
    _test_files_structure = {}
    _cache_file = os.path.join(work_directory, '.btt_cache.json')

    def __init__(self, pref, suff):
        self._file_scaner = FilesScaner(pref, suff)
        self._file_parser = FilesParser()

    def parse(self, folder_path, without_caching=False):
        """
        Searches for test files and parses them
        :param str folder_path: path to target folder
        :param bool without_caching:
        """
        self._file_scaner._scan(folder_path)

        if not self._file_scaner.files:
            message = color_output.warning('Nothing to parse - no test files\n')
            sys.stderr.write(message)
            return

        message = color_output.info('Number of test files: {}\n'.format(len(self._file_scaner.files)))
        sys.stderr.write(message)

        for filepath in self._file_scaner.files:
            self._test_files_structure[filepath] = self._file_parser._parse_file(filepath)

        message = color_output.succes('Parsing is completed\n')
        sys.stderr.write(message)

        if not without_caching:
            self._saves_cache()

    def show_test_structure(self):
        if os.path.exists(self._cache_file):
            with open(self._cache_file) as file:
                data = json.load(file)
                pprint(data)
        else:
            message = color_output.warning('Nothing to show. Before call this command run the "parse" command\n')
            sys.stderr.write(message)

    def _saves_cache(self):
        with open(self._cache_file, 'w') as outfile:
            json.dump(self._test_files_structure, outfile)

        message = color_output.info('Tests structure was cached\n')
        sys.stderr.write(message)
