import os

import fire

from bds_test_tool.launchers import AbstractLauncherFactory
from bds_test_tool.parser import ParserTests
from bds_test_tool.utils import ColorOutput

color_output = ColorOutput()
working_directory = os.path.dirname(os.path.realpath(__file__))


class Commands(ParserTests, AbstractLauncherFactory):
    def __init__(self, pref, suff):
        super(Commands, self).__init__(pref, suff)

    def help(self):
        with open(os.path.join(working_directory, 'help.tpl')) as file:
            text = file.readlines()
        color_output.info(''.join(text))


def main():
    commands = Commands(pref='test_', suff='.py')
    fire.Fire(commands)
