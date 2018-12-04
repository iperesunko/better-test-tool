import sys
from timeit import default_timer as timer

import pkg_resources


class ColorOutput:
    """
    The class contains methods for color outputting messages to the screen
    """

    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[94m'
    reset = '\033[0m'

    def error(self, text):
        """Displays error messages in the console"""
        sys.stderr.write(self.red + text + self.reset)

    def warning(self, text):
        """Displays warning messages in the console"""
        sys.stderr.write(self.yellow + text + self.reset)

    def succes(self, text):
        """Displays success messages in the console"""
        sys.stdout.write(self.green + text + self.reset)

    def info(self, text):
        """Displays info messages in the console"""
        sys.stdout.write(self.blue + text + self.reset)

    def standard(self, text):
        """Displays standard messages in the console"""
        sys.stdout.write(text)


# File configuration for caching
CACHE_FILENAME = '.btt_cache.json'


def search_statistics(func):
    """
    The decorator measures the time of searching for modules and displays brief statistics on the screen
    :param func:
    :return list:
    """

    def wrapper(*args, **kwargs):
        start_time = timer()
        results = func(*args, **kwargs)
        end_time = timer()

        execute_time = end_time - start_time
        message = '\033[32mFound results: {} in {:f} seconds\n\n\033[0m'.format(len(results), execute_time)
        sys.stdout.write(message)

        return results

    return wrapper


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
