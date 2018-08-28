# BDS Test Tool

### Requirements:
- Python >= 2.7 (Better working on Python >= 3.5)
- [python-fire](https://github.com/google/python-fire)

## Setup and usages
```bash
$ python setup.py install
$ btt help
```

## Commands

```markdown
btt parse {folder_path} - Parse a test folder
btt show-files - Shows  all tests files
btt find '{simplified path}' - Shows matched modules
btt {launcher_name} run '{simplified path}' - Finds and starts a test module
btt {launcher_name} generate '{simplified path}' - Generates a command for a manual start
```