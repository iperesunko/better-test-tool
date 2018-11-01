from better_test_tool.argument_parser import cli_parser
from better_test_tool.launchers import AbstractFabricLauncher
from better_test_tool.parser import ParserTests
from better_test_tool.utils import ColorOutput

color_output = ColorOutput()
file_parser = ParserTests()


def main():
    args = cli_parser.parse_args()
    if args.command == 'parse':
        file_parser.parse(args.path)
    else:
        launcher = AbstractFabricLauncher(args.command)
        return launcher.generate(module_path=args.path, method=args.method)


if __name__ == '__main__':
    main()