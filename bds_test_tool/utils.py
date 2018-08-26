class ColorOutput:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

    def error(self, text):
        return self.RED + text + self.RESET

    def warning(self, text):
        return self.YELLOW + text + self.RESET

    def succes(self, text):
        return self.GREEN + text + self.RESET

    def info(self, text):
        return self.BLUE + text + self.RESET
