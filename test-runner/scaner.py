import json
import logging
import os
import re
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


class FileParser:
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


class TestRunnerConstructor:
    test_files_structure = {}

    def __init__(self, pref, suff):
        self.file_scaner = FilesScaner(pref, suff)
        self.file_parser = FileParser()

    def parse_test_structure(self, folder_path):
        self.file_scaner.scan(folder_path)
        logging.info('Number of test files: {}'.format(len(self.file_scaner.files)))
        for filepath in self.file_scaner.files:
            self.test_files_structure[filepath] = self.file_parser.parse_file(filepath)
        logging.info('Search for files and their parsing is complete')

    def show_test_structure(self):
        pprint(self.test_files_structure)

    def save_cache(self):
        with open('test_runner_cache.json', 'w') as outfile:
            json.dump(self.test_files_structure, outfile)
        logging.info('Test structure was saved into file')


def main():
    test_runner = TestRunnerConstructor(pref='test_', suff='.py')
    test_runner.parse_test_structure('/home/ihor/dev/test')
    # test_runner.show_test_structure()
    test_runner.save_cache()


if __name__ == '__main__':
    main()
