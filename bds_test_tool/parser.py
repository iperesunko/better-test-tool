import json
import os
import re
import sys
from collections import defaultdict
from pprint import pprint


class FilesScaner:
    files = []

    def __init__(self, pref, suff):
        self.pref = pref
        self.suff = suff

    def scan(self, path):
        found_files = os.walk(path)

        for dirpath, _, filenames in found_files:
            for _file in filenames:
                if self.files_filter(_file):
                    self.files.append(os.path.join(dirpath, _file))

    def files_filter(self, file):
        if file.startswith(self.pref) and file.endswith(self.suff):
            return True

        return False

    def show_files(self):
        pprint(self.files)


class FilesParser:
    re_class = re.compile(r'class (\w+)')
    re_method = re.compile(r'\s+def (\w+)')
    re_function = re.compile(r'def (\w+)')

    def parse_file(self, path):
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
    test_files_structure = {}
    cache_file = 'test_runner_cache.json'

    def __init__(self, pref, suff):
        self.file_scaner = FilesScaner(pref, suff)
        self.file_parser = FilesParser()

    def parse(self, folder_path, without_caching=False):
        self.file_scaner.scan(folder_path)

        if not self.file_scaner.files:
            sys.stderr.write('Nothing to parse - folder is empty\n')
            return

        sys.stderr.write('Number of test files: {}\n'.format(len(self.file_scaner.files)))

        for filepath in self.file_scaner.files:
            self.test_files_structure[filepath] = self.file_parser.parse_file(filepath)
        sys.stderr.write('Parsing is completed\n')

        if not without_caching:
            self._saves_cache()

    def show_test_structure(self):
        # TODO: show cached tests structure (open json file)
        if self.test_files_structure:
            pprint(self.test_files_structure)
        else:
            sys.stderr.write('Nothing to show. Before call this command run the "parse" command\n')

    def _saves_cache(self):
        with open(self.cache_file, 'w') as outfile:
            json.dump(self.test_files_structure, outfile)
        sys.stderr.write('Tests structure was cached\n')
