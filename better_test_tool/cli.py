import click
import pyperclip

from better_test_tool import launchers, parser, utils, VERSION


def copy_to_clipboard(result):
    click.secho('Copied to clipboard', fg='blue')
    pyperclip.copy(result)


@click.group(help='Better Test Tool: Utility for simple testing projects')
@click.version_option(version=VERSION)
def cli():
    pass


@cli.command(help='parses a test folder structure and cache it')
@click.argument('path', type=click.Path(exists=True), autocompletion=utils.auto_complete_paths)
def parse(path):
    file_parser = parser.ParserTests()
    try:
        files_number = file_parser.parse(path)
    except utils.BTTError as error:
        click.secho(error.message, fg=error.color)
    else:
        click.secho('Parsing completed. Found {} files.'.format(files_number), fg='green')
        click.secho('Cache saved into "{}"'.format(utils.get_cache_filename()), fg='green')


def search_process(provider, path, method, copy):
    """
    Common search command realization for different test providers
    :param provider: provider class
    :param str path: path to modile
    :param str method: function or method name
    :param bool copy:
    :return:
    """
    try:
        result = provider.generate(path, method)
    except utils.BTTError as error:
        click.secho(error.message, fg=error.color)
    else:
        if result and copy:
            copy_to_clipboard(result)

        click.echo(result)


@cli.command(help='generates a command for manual execute in nosetests')
@click.argument('path')
@click.option('-m', '--method')
@click.option('-cp', '--copy', is_flag=True)
def nosetests(path, method, copy):
    search_process(launchers.NoseTestsLauncher(), path, method, copy)


@cli.command(help='generates a command for manual execute in pytest')
@click.argument('path')
@click.option('-m', '--method')
@click.option('-cp', '--copy', is_flag=True)
def pytest(path, method, copy):
    search_process(launchers.PytestLauncher(), path, method, copy)
