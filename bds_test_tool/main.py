import os

import fire

from bds_test_tool.launchers import Finder, NoseTestsLauncher
from bds_test_tool.parser import ParserTests
from bds_test_tool.utils import ColorOutput

color_output = ColorOutput()
working_directory = os.path.dirname(os.path.realpath(__file__))

parser = ParserTests()
finder = Finder()
nosetests = NoseTestsLauncher()


def help_message():
    with open(os.path.join(working_directory, 'help.tpl')) as file:
        text = file.readlines()
    color_output.info(''.join(text))


commands = {
    'parse': parser.parse,
    'show-files': parser.show_test_structure,
    'find': finder.find,
    'nosetests': nosetests,
    'help': help_message
}


def main():
    fire.Fire(commands)


if __name__ == '__main__':
    main()
