import json
import os

from bds_test_tool.launchers import BaseLauncher
from bds_test_tool.parser import ParserTests


class TestBaseLauncher:

    @classmethod
    def setup_class(cls):
        cls.base_launcher = BaseLauncher()
        cls.base_launcher._cache_file = '.btt_cache.json'

    @classmethod
    def teardown_class(cls):
        if os.path.exists('.btt_cache.json'):
            os.remove('.btt_cache.json')

    def test__open_cache_file_without_file(self):
        result = self.base_launcher._open_cache_file()
        assert result is False

    def test__open_cache_file(self):
        parser = ParserTests(pref='test_', suff='.py')
        parser._cache_file = '.btt_cache.json'
        parser.parse('file-fixtures')

        result = self.base_launcher._open_cache_file()
        assert result is True

        with open('.btt_cache.json') as file:
            data = json.load(file)
        assert data == self.base_launcher._files_structure
