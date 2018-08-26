from bds_test_tool.parser import ParserTests

import fire


def main():
    test_parser = ParserTests(pref='test_', suff='.py')
    fire.Fire(test_parser)
