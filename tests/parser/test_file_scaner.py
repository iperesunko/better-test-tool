import json
import os

import pytest

from better_test_tool import utils
from better_test_tool.parser import FilesParser, FilesScaner, ParserTests
from better_test_tool.utils import BTTError


class TestFilesScaner:
    def setup_method(self, method):
        self.files_scaner = FilesScaner()

    def test_scan(self):
        test_files = {
            'file-fixtures/test_config_server.py',
            'file-fixtures/test_skl_1.py',
            'file-fixtures/test_some_func.py',
            'file-fixtures/unit/server/test_config_server.py',
        }

        m_type = self.files_scaner.scan('file-fixtures')
        assert m_type == os.stat('file-fixtures').st_mtime
        assert test_files == set(self.files_scaner.files)

    def test_files_filter(self):
        files = (('test_come_func.py', True), ('other_test_file.py', False), ('not-python-file', False))

        for file, answer in files:
            assert answer == self.files_scaner.files_filter(file)


class TestFilesParser:
    def setup_method(self, method):
        self.files_parser = FilesParser()

    def test_parse_file(self):
        files = [
            'file-fixtures/test_config_server.py',
            'file-fixtures/test_skl_1.py',
            'file-fixtures/test_some_func.py',
            'file-fixtures/unit/server/test_config_server.py',
        ]

        parsed_files = [
            {'TestConfigServer': ['test_one_case', 'test_alpha_settings'], 'functions': ['test_configuration']},
            {'TestAlphaClass': ['test_d_suite', 'test_settings'], 'functions': ['test_case_one', 'test_some_test']},
            {'TestFunctional': ['test_one_case', 'test_other_case'], 'functions': ['test_case_without_class']},
            {'functions': ['test_initialize_ok_zk', 'test_add_invalid_path', 'test_add_duplicate']},
        ]

        for file, result in zip(files, parsed_files):
            assert result == self.files_parser.parse_file(file)


class TestParserTests:
    def setup_method(self, method):
        self.parser_test = ParserTests()
        self.parsed_structure = {
            'm_time': os.stat('file-fixtures').st_mtime,
            'test_folder': 'file-fixtures',
            'file-fixtures/test_config_server.py': {
                'TestConfigServer': ['test_one_case', 'test_alpha_settings'],
                'functions': ['test_configuration'],
            },
            'file-fixtures/test_skl_1.py': {
                'TestAlphaClass': ['test_d_suite', 'test_settings'],
                'functions': ['test_case_one', 'test_some_test'],
            },
            'file-fixtures/test_some_func.py': {
                'TestFunctional': ['test_one_case', 'test_other_case'],
                'functions': ['test_case_without_class'],
            },
            'file-fixtures/unit/server/test_config_server.py': {
                'functions': ['test_initialize_ok_zk', 'test_add_invalid_path', 'test_add_duplicate']
            },
        }

    def teardown_method(self, method):
        if os.path.exists(utils.get_cache_filename()):
            os.remove(utils.get_cache_filename())

    def test_parse(self):
        self.parser_test.parse('file-fixtures')
        assert os.path.exists(utils.get_cache_filename()) is True
        assert self.parser_test.test_files_structure == self.parsed_structure

        with open(utils.get_cache_filename()) as file:
            data = json.load(file)
        assert data == self.parsed_structure and data == self.parser_test.test_files_structure

    def test_parse_not_a_folder(self):
        with pytest.raises(BTTError):
            self.parser_test.parse('Makefile')

    def test_parse_path_does_not_exist(self):
        with pytest.raises(BTTError):
            self.parser_test.parse('some-stramge-path')
