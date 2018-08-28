import os
import sys
from timeit import default_timer as timer


class ColorOutput:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

    def error(self, text):
        sys.stderr.write(self.RED + text + self.RESET)

    def warning(self, text):
        sys.stderr.write(self.YELLOW + text + self.RESET)

    def succes(self, text):
        sys.stderr.write(self.GREEN + text + self.RESET)

    def info(self, text):
        sys.stderr.write(self.BLUE + text + self.RESET)


# File configuration for caching
cache_filename = '.btt_cache.json'
work_directory = os.path.dirname(os.path.realpath(__file__))
cache_file_path = os.path.join(work_directory, cache_filename)


def search_statistics(func):
    def wrapper(*args, **kwargs):
        start_time = timer()
        results = func(*args, **kwargs)
        end_time = timer()

        execute_time = end_time - start_time
        message = '\033[32mFound results: {} in {:f} seconds\n\n\033[0m'.format(len(results), execute_time)
        sys.stderr.write(message)

        return results

    return wrapper
