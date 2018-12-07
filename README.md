# Better Test Tool: Utility for simple testing projects

[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/iperesunko/better-test-tool)

![](https://media.giphy.com/media/elMZLkephFAIobrgIS/giphy.gif)

## Description

Helps generate commands for running specific tests

Supports pytest and nose

Supports Python 2.7 and Python >= 3.5

Tested on Linux

## Installation
```bash
$ git clone https://github.com/iperesunko/better-test-tool.git
$ python setup.py install --user

# or
$ pip install git+https://github.com/iperesunko/better-test-tool.git --user
```

### Autocompletion
For bash users add this to your `.bashrc`:
```sh
eval "$(_BTT_COMPLETE=source btt)"
```

For zsh users add this to your `.zshrc`:

```sh
eval "$(_BTT_COMPLETE=source_zsh btt)"
```

> Add the cache file (.btt-cache.json) to **.gitignore** (must be committed) or add to the exclusion file **.git/info/exclude** in project folder

## Commands:
```bash
$ btt --help
```

- **parse** - parses a test folder structure and cache it (the command must be called at the first use and/or when the test structure has changed)
- **nosetests** - generates a command for manual execute in nosetests
- **pytest** - generates a command for manual execute in pytest
- optional arguments
    - **--method or -m** - used with runners (nosetests or pytest commands). allows you to specify the name of the test case 
    - **--copy or -cp** - copy result to clipboard

> If several matches are found with the names, you will be offered the choice of a module and a test case.

## Examples:
```bash
$ btt parse test
Parsing completed. Found 104 files.

$ btt nosetests "functional config server"
nosetests test/functional/test_config_server.py

$ btt nosetests "db utils" -m "open conn"
nosetests -svv test/test_db_utils.py:TestFreeTDSBackend.test_open_nonexistent_connection

$ btt pytest "func config server"
pytest test/functional/test_config_server.py -v

$ btt pytest "db utils" -m "close conn"
pytest test/test_db_utils.py::TestBackendConnectionFabric::test_open_close_postgre_connection -v
```