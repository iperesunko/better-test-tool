import pyperclip

from better_test_tool.argument_parser import cli_parser
from better_test_tool.launchers import AbstractFabricLauncher
from better_test_tool.parser import ParserTests
from better_test_tool.utils import ColorOutput, get_version

color_output = ColorOutput()
file_parser = ParserTests()


def main():
    args = cli_parser.parse_args()
    if args.version:
        return color_output.info('Better test tool {}\n'.format(get_version()))
    elif not args.command:
        return cli_parser.print_help()
    elif args.command == 'parse':
        file_parser.parse(args.path)
    else:
        launcher = AbstractFabricLauncher(args.command)
        result = launcher.generate(module_path=args.path, method=args.method)
        if args.copy:
            color_output.info('Copied to clipboard\n')
            pyperclip.copy(result)

        return result


if __name__ == '__main__':
    main()
