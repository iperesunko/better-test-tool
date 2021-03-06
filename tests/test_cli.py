import os

from click.testing import CliRunner

from better_test_tool import utils
from better_test_tool.cli import cli, nosetests, parse, pytest


class TestCLI:
    def setup_method(self, method):
        self.runner = CliRunner()

    def remove_cache(self):
        if os.path.exists(utils.get_cache_filename()):
            os.remove(utils.get_cache_filename())

    def teardown_method(self, method):
        self.remove_cache()

    def test_version(self):
        result = self.runner.invoke(cli, '--version')
        assert result.exit_code == 0
        assert 'version' in result.output

    def test_parse(self):
        result = self.runner.invoke(parse, 'file-fixtures')
        assert result.exit_code == 0
        assert (
                'Parsing completed. Found 4 files.\n'
                'Cache saved into "{}"\n'.format(utils.get_cache_filename())
                == result.output)

    def test_parse_no_test_files(self):
        result = self.runner.invoke(parse, 'better_test_tool')
        assert result.exit_code == 0
        assert 'Nothing to parse - no test files\n' == result.output

    def test_parse_folder_do_not_exists(self):
        result = self.runner.invoke(parse, 'better-test-tool')
        assert result.exit_code == 2

    def test_parse_not_a_folder(self):
        result = self.runner.invoke(parse, 'README.md')
        assert result.exit_code == 0
        assert 'This is not a folder\n' == result.output

    def test_nosetests_no_cache(self):
        self.remove_cache()
        result = self.runner.invoke(nosetests, 'skl')
        assert result.exit_code == 0
        assert 'Cache file not found. First run the command "btt parse folderpath"' in result.output

    def test_pytest_no_cache(self):
        self.remove_cache()
        result = self.runner.invoke(pytest, 'skl')
        assert result.exit_code == 0
        assert 'Cache file not found. First run the command "btt parse folderpath"' in result.output

    def test_nosetests(self):
        self.runner.invoke(parse, 'file-fixtures')
        result = self.runner.invoke(nosetests, 'skl')
        assert result.exit_code == 0
        assert result.output == 'nosetests -svv file-fixtures/test_skl_1.py\n'

    def test_nosetests_method(self):
        self.runner.invoke(parse, 'file-fixtures')
        result = self.runner.invoke(nosetests, ['some func', '-m', 'other case'])
        assert result.exit_code == 0
        assert result.output == 'nosetests -svv file-fixtures/test_some_func.py:TestFunctional.test_other_case\n'

    def test_nosetests_not_found(self):
        self.runner.invoke(parse, 'file-fixtures')
        result = self.runner.invoke(nosetests, ['skl', '-m', 'other case'])
        assert result.exit_code == 0
        assert 'No matches found.' in result.output

    def test_nosetests_copy(self):
        self.runner.invoke(parse, 'file-fixtures')
        result = self.runner.invoke(nosetests, ['skl', '-m', 'settings', '-cp'])
        assert result.exit_code == 0
        assert 'Copied to clipboard' in result.output
        assert 'nosetests -svv file-fixtures/test_skl_1.py:TestAlphaClass.test_settings\n'

    def test_pytest(self):
        self.runner.invoke(parse, 'file-fixtures')
        result = self.runner.invoke(pytest, 'skl')
        assert result.exit_code == 0
        assert result.output == 'pytest file-fixtures/test_skl_1.py -v\n'

    def test_pytest_method(self):
        self.runner.invoke(parse, 'file-fixtures')
        result = self.runner.invoke(pytest, ['some func', '-m', 'other case'])
        assert result.exit_code == 0
        assert result.output == 'pytest file-fixtures/test_some_func.py::TestFunctional::test_other_case -v\n'

    def test_pytest_not_found(self):
        self.runner.invoke(parse, 'file-fixtures')
        result = self.runner.invoke(pytest, ['skl', '-m', 'other case'])
        assert result.exit_code == 0
        assert 'No matches found.' in result.output

    def test_pytest_copy(self):
        self.runner.invoke(parse, 'file-fixtures')
        result = self.runner.invoke(pytest, ['skl', '-m', 'settings', '-cp'])
        assert result.exit_code == 0
        assert 'Copied to clipboard' in result.output
        assert 'pytest file-fixtures/test_skl_1.py::TestAlphaClass::test_settings -v\n'

    def test_pytest_no_result_copy(self):
        result = self.runner.invoke(pytest, ['skl', '-m', 'setup', '-cp'])
        assert result.exit_code == 0
        assert 'Copied to clipboard' not in result.output
        assert 'No matches found.' in result.output
