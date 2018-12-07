import json
import os
import sys
import time

import pytest

from better_test_tool.launchers import Finder
from better_test_tool.parser import ParserTests
from better_test_tool.utils import BTTError


class TestFinder:
    def setup_method(self, method):
        self.finder = Finder()

    def teardown_method(self, method):
        if os.path.exists('.btt_cache.json'):
            os.remove('.btt_cache.json')

    @staticmethod
    def do_parse():
        parser = ParserTests()
        parser.parse('file-fixtures')

    def test__generate_regex(self):
        expected = ('.*unit.*', '.*extract.*pstn.*', '.*.py.*', '.*regress.*transf.*cme.*')

        data = ('unit', 'extract pstn', '.py', 'regress transf cme')

        for path, expect in zip(data, expected):
            assert expect == self.finder._generate_regex(path)

    def test_cache_load_ok(self):
        self.do_parse()
        assert hasattr(self.finder, '_files_structure') is True

    def test_cache_load_without_cache(self, capsys):
        with pytest.raises(BTTError):
            hasattr(self.finder, '_files_structure')

    def test_cache_auto_update(self):
        self.do_parse()
        with open('.btt_cache.json', 'r') as file:
            test_data = json.load(file)

        rigth_time = test_data.get('m_time')
        new_time = {'m_time': time.time()}
        test_data.update(new_time)
        with open('.btt_cache.json', 'w') as file:
            json.dump(test_data, file)

        assert rigth_time == self.finder._files_structure.get('m_time')

    def test_finds_modules(self):
        matched_modules = {'file-fixtures/test_config_server.py', 'file-fixtures/unit/server/test_config_server.py'}
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

    def test_find_tests(self):
        expected_tests = {
            'TestConfigServer test_one_case',
            'TestConfigServer test_alpha_settings',
            'functions test_configuration',
        }
        self.do_parse()
        result = self.finder.find_tests('file-fixtures/test_config_server.py', 'test')
        assert set(result) == expected_tests

        expected_tests = {
            'TestFunctional test_one_case',
            'TestFunctional test_other_case',
            'functions test_case_without_class',
        }
        result = self.finder.find_tests('file-fixtures/test_some_func.py', 'case')
        assert set(result) == expected_tests

    def test_item_selection_many_items(self, capsys):
        large_list = [i for i in range(11)]
        with pytest.raises(BTTError):
            self.finder.item_selection(large_list)

    def test_item_selection_one_item(self):
        result = self.finder.item_selection(['one'])
        assert result == 'one'

    def test_item_selection_no_modules(self, capsys):
        with pytest.raises(BTTError):
            self.finder.item_selection([])

    def test_item_selection_several_items(self, capsys, monkeypatch):
        fake_modules = ['one', 'two', 'three', 'four', 'five']

        # mocking a stdin readline method
        def fake_stdin():
            return '4'

        monkeypatch.setattr(sys.stdin, 'readline', fake_stdin)

        result = self.finder.item_selection(fake_modules)
        captured = capsys.readouterr()

        assert result == 'four'
        assert 'Several modules were found, select the required one:\n' in captured.out
