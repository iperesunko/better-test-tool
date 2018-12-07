import os

import pkg_resources


class BTTError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__()
        self.message = message

    def __str__(self):
        return self.message


# File configuration for caching
CACHE_FILENAME = '.btt_cache.json'


def format_multuple_modules(modules):
    """
    Forms the numbered output of modules from the list
    :param list modules: list of modules paths
    :return str:
    """
    return '\n'.join(['{}. {}'.format(index, name) for index, name in enumerate(modules, 1)])


def get_version():
    """
    Returns a utility version
    :return str: '0.5'
    """
    return pkg_resources.require('better_test_tool')[0].version


def check_test_folder(test_folder):
    """
    Checks if the specified path exists and if it is a folder
    :param str test_folder: path to folder
    :return: Raises BTTError if not
    """
    if not os.path.exists(test_folder):
        raise BTTError('Path does not exists')
    elif not os.path.isdir(test_folder):
        raise BTTError('This is not a folder')


def is_folder_modified(m_time, test_folder):
    """
    Compares the specified time with the current
    content modification time.
    :param float m_time: specified time
    :param str test_folder: path to folder
    :return bool: True if time does not match otherwise False
    """
    actual_time = get_folder_time(test_folder)
    return not (actual_time == m_time)


def get_folder_time(test_folder):
    """
    Gets a folder modified content time
    :param str test_folder: path to folder
    :return float: timestamp
    """
    check_test_folder(test_folder)
    return os.stat(test_folder).st_mtime
