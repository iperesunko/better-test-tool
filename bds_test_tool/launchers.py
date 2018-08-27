import json
import os

from bds_test_tool.utils import ColorOutput

color_output = ColorOutput()


class BaseLauncher(object):
    _files_structure = None

    def _open_cache_file(self):
        work_directory = os.path.dirname(os.path.realpath(__file__))
        _cache_file = os.path.join(work_directory, '.btt_cache.json')

        if os.path.exists(_cache_file):
            with open(_cache_file) as file:
                self._files_structure = json.load(file)
            return True
        else:
            color_output.error('Cache file not found. First run the command "btt parse folderpath"\n')
            return False

    def generate_command(self, simplified_path):
        raise NotImplemented

    def run(self, simplified_path):
        raise NotImplemented


class NoseTestLauncher(BaseLauncher):
    def generate_command(self, simplified_path):
        if self._open_cache_file():
            color_output.succes('Nose test generate a command\n')
        else:
            color_output.error('Nose test do not generate a command\n')

    def run(self, simplified_path):
        if self._open_cache_file():
            color_output.succes('Nose test run test\n')
        else:
            color_output.error('Nose test do not run test\n')


class AbstractLauncherFactory(object):
    nosetest = NoseTestLauncher()
