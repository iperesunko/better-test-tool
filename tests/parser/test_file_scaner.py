from bds_test_tool.parser import FilesParser, FilesScaner


class TestFilesScaner:

    def setup_class(cls):
        cls.files_scaner = FilesScaner('test_', '.py')

    def test_scan(self):
        test_files = [
            'file-fixtures/test_skl_1.py',
            'file-fixtures/test_some_func.py',
            'file-fixtures/unit/server/test_server.py',
        ]

        self.files_scaner.scan('file-fixtures')
        self.files_scaner.show_files()
        assert test_files == self.files_scaner.files

    def test_files_filter(self):
        files = (
            ('test_come_func.py', True),
            ('other_test_file.py', False),
            ('not-python-file', False),
        )

        for file, answer in files:
            assert answer == self.files_scaner.files_filter(file)


class TestFilesParser:
    def setup_class(cls):
        cls.files_parser = FilesParser()

    def test_parse_file(self):
        files = [
            'file-fixtures/test_skl_1.py',
            'file-fixtures/test_some_func.py',
            'file-fixtures/unit/server/test_server.py',
        ]

        parsed_files = [
            {
                'TestAlphaClass': [
                    'test_d_suite',
                    'test_settings',
                ],
                'functions': [
                    'test_case_one',
                    'test_some_test',
                ]
            },
            {
                'TestFunctional': [
                    'test_one_case',
                    'test_other_case',
                ],
                'functions': [
                    'test_case_without_class'
                ]
            },
            {
                'functions': [
                    'test_initialize_ok_zk',
                    'test_add_invalid_path',
                    'test_add_duplicate',
                ],
            }
        ]

        for file, result in zip(files, parsed_files):
            assert result == self.files_parser.parse_file(file)
