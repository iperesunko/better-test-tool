import argparse

from bds_test_tool.parser import ParserTests

file_parser = ParserTests()

cli_parser = argparse.ArgumentParser(prog='btt', description='A tool for easy testing the Billing Data Server')
cli_parser.add_argument('--version', '-v', action='store_true', help='show version')
subparsers = cli_parser.add_subparsers(title='Commands', dest='command')

# parse command
parse_command = subparsers.add_parser('parse', help='parses a test folder structure and cache it')
parse_command.add_argument('path')

# commands for launchers
nosetests_command = subparsers.add_parser('nosetests', help='generates a command for manual execute in nosetests')
nosetests_command.add_argument('path', help='simplified path for finding a module')
nosetests_command.add_argument('--method', '-m', help='simplified path for finding a func or method')

pytest_comand = subparsers.add_parser('pytest', help='generates a command for manual execute in pytest')
pytest_comand.add_argument('path', help='simplified path for finding a module')
pytest_comand.add_argument('--method', '-m', help='simplified path for finding a func or method')
