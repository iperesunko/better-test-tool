from parser import ParserTests

import fire

if __name__ == '__main__':
    test_parser = ParserTests(pref='test_', suff='.py')
    fire.Fire(test_parser)
