import pytest

from better_test_tool import utils


def test_get_folder_time():
    result = utils.get_folder_time('file-fixtures')
    assert result == 1544035211.4587939


def test_is_folder_modified():
    result = utils.is_folder_modified(1544035211.4587939, 'file-fixtures')
    assert result is False

    result = utils.is_folder_modified(1544041029.8485782, 'file-fixtures')
    assert result is True


def test_check_test_folder():
    utils.check_test_folder('tests')


def test_check_test_folder_not_folder():
    with pytest.raises(utils.BTTError):
        utils.check_test_folder('Makefile')


def test_check_test_folder_not_exists():
    with pytest.raises(utils.BTTError):
        utils.check_test_folder('some-test-folder')


def test_format_multuple_modules():
    modules = ['test', 'test/one', 'test/one/two']
    expected = '1. test\n2. test/one\n3. test/one/two'
    result = utils.format_multuple_modules(modules)
    assert result == expected


def test_filter_folders():
    folders = ['tests', 'file-fixtures', 'better-test-code']
    assert ['tests'] == utils.filter_folders(folders, 'te')


@pytest.fixture
def get_search_word():
    return 'fil'


def test_auto_complete_paths():
    utils.get_search_word = get_search_word
    assert ['file-fixtures'] == utils.auto_complete_paths(None, None, None)


def test_is_access():
    assert utils.is_access('tests') is True
    assert utils.is_access('/root') is False
