BDS Test Tool (btt) - A tool for easy testing the Billing Data Server

Usages:
    btt {command} {--optional_argumets argument}
    e.g. btt parse tests/

Commands:
    parse {folder_path} [--without_cache=True] - parse a test folder

    show_test_structure - show tests structure

    {launcher_name} run {'simplified_path'} - finds and starts a test module (or test case in test module)
    e.g. btt nosetest run 'unit config_server test_01'

    {launcher_name} generate_command {'simplified_path'} - finds a test and generates a command for a manual start

Launchers:
    nosetest - Not Implemented
    regression - Not Implemented
    pytest - Not Implemented
