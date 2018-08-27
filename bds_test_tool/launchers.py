import json
import os

from bds_test_tool.utils import ColorOutput, cache_file_path

color_output = ColorOutput()


class BaseLauncher(object):
    _cache_file = cache_file_path

    def __init__(self):
        self._files_structure = None

    def _open_cache_file(self):
        if isinstance(self._files_structure, dict):
            return True

        if os.path.exists(self._cache_file):
            with open(self._cache_file) as file:
                self._files_structure = json.load(file)
            return True
        else:
            color_output.error('Cache file not found. First run the command "btt parse folderpath"\n')
            return False

    def _check_compliance(self, file_path, simplified_path):
        """
        Checks the path of the module for matching with the specified names
        :param str file_path: 'file-fixtures/unit/server/test_config_server.py'
        :param simplified_path: 'unit server config_server'
        :return bool: True or False
        """
        for name in simplified_path.split(' '):
            if name not in file_path:
                break
        else:
            return True

        return False

    def _find_test_module(self, simplified_path):
        matching = []
        modules = self._files_structure.keys()

        for module in modules:
            if self._check_compliance(module, simplified_path):
                matching.append(module)

        return matching

    def _format_multuple_modules(self, modules):
        return '\n'.join(['{}. {}'.format(index, name) for index, name in enumerate(modules, 1)])

    def generate_command(self, simplified_path):
        raise NotImplemented

    def run(self, simplified_path):
        raise NotImplemented


class NoseTestLauncher(BaseLauncher):
    def generate_command(self, simplified_path):
        if self._open_cache_file():
            modules = self._find_test_module(simplified_path)
            if 1 > len(modules) <= 10:
                formatted = self._format_multuple_modules(modules)
                message = 'Several modules were found, select the required one:\n' + formatted
                color_output.info(message + '\n')

    def run(self, simplified_path):
        if self._open_cache_file():
            color_output.succes('Nose test run test\n')
        else:
            color_output.error('Nose test do not run test\n')


class AbstractLauncherFactory(object):
    nosetest = NoseTestLauncher()
