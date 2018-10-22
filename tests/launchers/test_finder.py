import os

import pytest

from bds_test_tool.launchers import Finder
from bds_test_tool.parser import ParserTests


class TestFinder:

    def setup_method(self, method):
        self.finder = Finder()

    def teardown_method(self, method):
        if os.path.exists('.btt_cache.json'):
            os.remove('.btt_cache.json')

    def do_parse(self):
        parser = ParserTests()
        parser.parse('file-fixtures')

    def test__generate_regex(self):
        expected = (
            '.*unit.*',
            '.*extract.*pstn.*',
            '.*.py.*',
            '.*regress.*transf.*cme.*'
        )

        data = (
            'unit',
            'extract pstn',
            '.py',
            'regress transf cme'
        )

        for path, expect in zip(data, expected):
            assert expect == self.finder._generate_regex(path)

    def test_cache_load_ok(self):
        self.do_parse()
        assert hasattr(self.finder, '_files_structure') is True

    def test_cache_load_without_cache(self, capsys):
        with pytest.raises(SystemExit):
            hasattr(self.finder, '_files_structure')
        captured = capsys.readouterr()
        assert 'Cache file not found. First run the command "btt parse folderpath"\n' in captured.err

    def test__finds_modules(self):
        matched_modules = {
            'file-fixtures/test_config_server.py',
            'file-fixtures/unit/server/test_config_server.py'
        }
        self.do_parse()
        result = set(self.finder.finds_modules('config_server'))
        assert result == matched_modules

        result = set(self.finder.finds_modules('unit config_server'))
        assert result == {'file-fixtures/unit/server/test_config_server.py'}

        matched_modules = {
            'file-fixtures/test_config_server.py',
            'file-fixtures/test_skl_1.py',
            'file-fixtures/test_some_func.py',
            'file-fixtures/unit/server/test_config_server.py',
        }
        result = set(self.finder.finds_modules('.py'))
        assert result == matched_modules

        result = set(self.finder.finds_modules('unit'))
        assert result == {'file-fixtures/unit/server/test_config_server.py'}

        result = set(self.finder.finds_modules('skl2'))
        assert result == set()
