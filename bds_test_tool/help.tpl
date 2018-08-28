BDS Test Tool (btt) - A tool for easy testing the Billing Data Server

Usages:
    btt {command} {--optional_argumets argument}
    e.g. btt parse tests/

Commands:
    btt parse {folder_path} - Parse a test folder
    btt show-files - Shows  all tests files
    btt find '{simplified path}' - Shows matched modules

    btt {launcher_name} run '{simplified path}' - Finds and starts a test module
    e.g. btt nosetests run 'unit config_server'

    btt {launcher_name} generate '{simplified path}' - Generates a command for a manual start
    btt help - Shows this message

Launchers:
    nosetests:
        run         Not Implemented
        generate    Implemented
    regression
        run         Not Implemented
        generate    Not Implemented
    pytest
        run         Not Implemented
        generate    Not Implemented
