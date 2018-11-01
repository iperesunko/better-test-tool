import os
import sys

from better_test_tool.launchers import BaseLauncher
from tests.launchers.test_finder import TestFinder


class TestBaseLauncher:
    def setup_method(self, method):
        self.base_launcher = BaseLauncher()
        self.base_launcher.module_separator = '#'
        self.base_launcher.test_case_separator = '^'
        self.base_launcher.command_template = 'abs-launcher {target}'

    def teardown_method(self, method):
        if os.path.exists('.btt_cache.json'):
            os.remove('.btt_cache.json')

    def test_cleanup(self):
        assert self.base_launcher.cleanup('TestClass some_method') == 'TestClass some_method'
        assert self.base_launcher.cleanup('functions test_case') == 'test_case'

    def test_target_formation(self):
        result = self.base_launcher.target_formation('/some/test/module.py', 'TestClass some_test_case')
        assert result == '/some/test/module.py#TestClass^some_test_case'

        result = self.base_launcher.target_formation('/some/test/module.py', 'functions test_case')
        assert result == '/some/test/module.py#test_case'

    def test_generate_one_module(self):
        TestFinder.do_parse()
        result = self.base_launcher.generate(module_path='some func')
        assert result == 'abs-launcher file-fixtures/test_some_func.py'

    def test_generate_several_modules(self, monkeypatch):
        TestFinder.do_parse()

        def fake_readline():
            return '2'

        monkeypatch.setattr(sys.stdin, 'readline', fake_readline)
        result = self.base_launcher.generate('config server')
        assert result == 'abs-launcher file-fixtures/unit/server/test_config_server.py'

    def test_generate_with_method(self):
        TestFinder.do_parse()
        result = self.base_launcher.generate(module_path='some func', method='one case')
        assert result == 'abs-launcher file-fixtures/test_some_func.py#TestFunctional^test_one_case'

        result = self.base_launcher.generate(module_path='some func', method='without class')
        assert result == 'abs-launcher file-fixtures/test_some_func.py#test_case_without_class'

    def test_generate_with_several_methods(self, monkeypatch):
        TestFinder.do_parse()

        def fake_readline():
            return '1'

        monkeypatch.setattr(sys.stdin, 'readline', fake_readline)
        result = self.base_launcher.generate(module_path='some func', method='case')
        assert result == 'abs-launcher file-fixtures/test_some_func.py#TestFunctional^test_one_case'

    def test_generate_with_several_modules_and_methods(self, monkeypatch, capsys):
        TestFinder.do_parse()

        def fake_readline():
            return '2'

        monkeypatch.setattr(sys.stdin, 'readline', fake_readline)
        result = self.base_launcher.generate(module_path='config server', method='add')
        captured = capsys.readouterr()

        assert result == 'abs-launcher file-fixtures/unit/server/test_config_server.py#test_add_duplicate'
        assert 'Several modules were found, select the required one:' in captured.out
        assert 'Several test cases were found, select the required one:' in captured.out
