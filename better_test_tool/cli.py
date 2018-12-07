import click
import pyperclip

from better_test_tool.launchers import NoseTestsLauncher, PytestLauncher
from better_test_tool.parser import ParserTests
from better_test_tool.utils import BTTError, auto_complete_paths, get_version


def copy_to_clipboard(result):
    click.secho('Copied to clipboard', fg='blue')
    pyperclip.copy(result)


@click.group(help='Better Test Tool: Utility for simple testing projects')
@click.version_option(version=get_version())
def cli():
    pass


@cli.command(help='parses a test folder structure and cache it')
@click.argument('path', type=click.Path(exists=True), autocompletion=auto_complete_paths)
def parse(path):
    file_parser = ParserTests()
    try:
        files_number = file_parser.parse(path)
    except BTTError as error:
        click.secho(error.message, fg=error.color)
    else:
        click.secho('Parsing completed. Found {} files.'.format(files_number), fg='green')


@cli.command(help='generates a command for manual execute in nosetests')
@click.argument('path')
@click.option('-m', '--method')
@click.option('-cp', '--copy', is_flag=True)
def nosetests(path, method, copy):
    nose_launcher = NoseTestsLauncher()
    try:
        result = nose_launcher.generate(path, method)
    except BTTError as error:
        click.secho(error.message, fg=error.color)
    else:
        if result and copy:
            copy_to_clipboard(result)

        click.echo(result)


@cli.command(help='generates a command for manual execute in pytest')
@click.argument('path')
@click.option('-m', '--method')
@click.option('-cp', '--copy', is_flag=True)
def pytest(path, method, copy):
    pytest_launcher = PytestLauncher()
    try:
        result = pytest_launcher.generate(path, method)
    except BTTError as error:
        click.secho(error.message, fg=error.color)
    else:
        if result and copy:
            copy_to_clipboard(result)

        click.echo(result)
