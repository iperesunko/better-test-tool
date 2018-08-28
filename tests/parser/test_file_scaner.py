import json
import os

from bds_test_tool.parser import FilesParser, FilesScaner, ParserTests


class TestFilesScaner:

    def setup_method(self, method):
        self.files_scaner = FilesScaner('test_', '.py')

    def test_scan(self):
        test_files = {
            'file-fixtures/test_config_server.py',
            'file-fixtures/test_skl_1.py',
            'file-fixtures/test_some_func.py',
            'file-fixtures/unit/server/test_config_server.py',
        }

        self.files_scaner._scan('file-fixtures')
        assert test_files == set(self.files_scaner.files)

    def test_files_filter(self):
        files = (
            ('test_come_func.py', True),
            ('other_test_file.py', False),
            ('not-python-file', False),
        )

        for file, answer in files:
            assert answer == self.files_scaner._files_filter(file)


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
            {
                'TestConfigServer': [
                    'test_one_case',
                    'test_alpha_settings',
                ],
                'functions': [
                    'test_configuration',
                ]
            },
            {
                'TestAlphaClass': [
                    'test_d_suite',
                    'test_settings',
                ],
                'functions': [
                    'test_case_one',
                    'test_some_test',
                ]
            },
            {
                'TestFunctional': [
                    'test_one_case',
                    'test_other_case',
                ],
                'functions': [
                    'test_case_without_class'
                ]
            },
            {
                'functions': [
                    'test_initialize_ok_zk',
                    'test_add_invalid_path',
                    'test_add_duplicate',
                ],
            }
        ]

        for file, result in zip(files, parsed_files):
            assert result == self.files_parser._parse_file(file)


class TestParserTests:

    def setup_method(self, method):
        self.parser_test = ParserTests(pref='test_', suff='.py')
        self.parser_test._cache_file = '.btt_cache.json'
        self.parsed_structure = {
            'file-fixtures/test_config_server.py': {
                'TestConfigServer': [
                    'test_one_case',
                    'test_alpha_settings',
                ],
                'functions': [
                    'test_configuration',
                ]
            },
            'file-fixtures/test_skl_1.py': {
                'TestAlphaClass': [
                    'test_d_suite',
                    'test_settings',
                ],
                'functions': [
                    'test_case_one',
                    'test_some_test',
                ]
            },
            'file-fixtures/test_some_func.py': {
                'TestFunctional': [
                    'test_one_case',
                    'test_other_case',
                ],
                'functions': [
                    'test_case_without_class'
                ]
            },
            'file-fixtures/unit/server/test_config_server.py': {
                'functions': [
                    'test_initialize_ok_zk',
                    'test_add_invalid_path',
                    'test_add_duplicate',
                ],
            }
        }

    def teardown_method(self, method):
        if os.path.exists('.btt_cache.json'):
            os.remove('.btt_cache.json')

    def test_parse_without_cache(self):
        self.parser_test.parse('file-fixtures', without_caching=True)
        assert os.path.exists('.btt_cache.json') is False
        assert self.parser_test._test_files_structure == self.parsed_structure

    def test_parse_with_cache(self):
        self.parser_test.parse('file-fixtures')
        assert os.path.exists('.btt_cache.json') is True
        assert self.parser_test._test_files_structure == self.parsed_structure

        with open('.btt_cache.json') as file:
            data = json.load(file)
        assert data == self.parsed_structure and data == self.parser_test._test_files_structure
