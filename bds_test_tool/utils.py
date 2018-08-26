import sys


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
