import os

import pkg_resources


class BTTError(Exception):
    def __init__(self, message, color='red'):
        super(Exception, self).__init__()
        self.message = message
        self.color = color

    def __str__(self):
        return self.message


def get_cache_folder():
    """
    Returns the path for the directory where the cache files will be stored.
    If the folder does not exist, it creates it.
    :return str: folder path
    """
    current_user = os.getlogin()
    cache_folder = '/home/{}/.cache/btt'.format(current_user)
    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)
    return cache_folder


def get_project_name():
    """
    Gets the name of the folder from which the utility is called
    :return str: folder name
    """
    return os.getcwd().split('/')[-1]


def get_cache_filename():
    """
    Returns the path and name of the cache file for the current project
    :return str: cache file path
    """
    filename = '{}.json'.format(get_project_name())
    return os.path.join(get_cache_folder(), filename)


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


def is_access(path):
    """

    :param path:
    :return:
    """
    if not os.access(path, os.R_OK):
        return False

    return True


def get_dirs(path):
    """
    Returns a list with folders
    :param str path:
    :return list: list of dirs
    """
    dirs = []
    for x in os.listdir(path):
        if is_access(x) and os.path.isdir(x):
            dirs.append(x)
    return dirs


def get_search_word():
    """
    Return a last COMP_WORDS item
    :return str or bool: item or False
    """
    word = os.environ['COMP_WORDS'].split()[2:]
    if not word:
        return False

    return word[0]


def filter_folders(folders, word):
    items = []
    for folder in folders:
        if os.path.normcase(folder).startswith(word):
            items.append(folder)
    return items


def auto_complete_paths(ctx, args, incomplete):
    """
    Prompts folder names in the current directory
    :param ctx: click context
    :param args: command arguments
    :param incomplete:
    :return list: matching folder list
    """
    folder_list = get_dirs('.')
    search_word = get_search_word()
    if not search_word:
        return folder_list
    else:
        return filter_folders(folder_list, search_word)
