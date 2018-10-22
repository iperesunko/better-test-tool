# BDS Test Tool

### Requirements:
- Python >= 2.7 (better working on Python >= 3.5)

## Setup and usages
```bash
$ python setup.py install --user
$ btt --help
```

Commands:
- **parse** - parses a test folder structure and cache it
    - `btt parse <path/to/test-folder>`
- **nosetests** - generates a command for manual execute in nosetests
    - `btt nosetests <"simplified module path">`
    - `btt nosetests "functional config server"` - for example return `nosetests test/functional/test_config_server.py`
- **pytest** - generates a command for manual execute in pytest
    - `btt pytest <"simplified module path">`
    - `btt pytest "unit utils"` - for example return `pytest test/unit/test_utils.py`

