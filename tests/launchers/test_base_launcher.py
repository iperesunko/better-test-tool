import json
import os

from bds_test_tool.launchers import BaseLauncher
from bds_test_tool.parser import ParserTests


class TestBaseLauncher:

    def setup_method(self, method):
        self.base_launcher = BaseLauncher()
        self.base_launcher._cache_file = '.btt_cache.json'

    def teardown_method(self, method):
        if os.path.exists('.btt_cache.json'):
            os.remove('.btt_cache.json')

    def do_parse(self):
        parser = ParserTests(pref='test_', suff='.py')
        parser._cache_file = '.btt_cache.json'
        parser.parse('file-fixtures')

    def test__open_cache_file_without_file(self):
        result = self.base_launcher._open_cache_file()
        assert result is False

    def test__open_cache_file(self):
        self.do_parse()

        result = self.base_launcher._open_cache_file()
        assert result is True

        with open('.btt_cache.json') as file:
            data = json.load(file)
        assert data == self.base_launcher._files_structure

    def test__finds_modules(self):
        matched_modules = {
            'file-fixtures/test_config_server.py',
            'file-fixtures/unit/server/test_config_server.py'
        }
        self.do_parse()
        self.base_launcher._open_cache_file()
        result = set(self.base_launcher._finds_modules('config_server'))
        assert result == matched_modules

        result = set(self.base_launcher._finds_modules('unit config_server'))
        assert result == {'file-fixtures/unit/server/test_config_server.py'}

        matched_modules = {
            'file-fixtures/test_config_server.py',
            'file-fixtures/test_skl_1.py',
            'file-fixtures/test_some_func.py',
            'file-fixtures/unit/server/test_config_server.py',
        }
        result = set(self.base_launcher._finds_modules('.py'))
        assert result == matched_modules

        result = set(self.base_launcher._finds_modules('unit'))
        assert result == {'file-fixtures/unit/server/test_config_server.py'}

        result = set(self.base_launcher._finds_modules('skl2'))
        assert result == set()
