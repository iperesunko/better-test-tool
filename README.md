# BDS Test Tool

### Requirements:
- Python >= 2.7 (better working on Python >= 3.5)
- pytest (for develop)

## Setup and usages
```bash
$ python setup.py install --user
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