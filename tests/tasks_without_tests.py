#! /usr/bin/python

import os
import re

TASK_DIR = 'tasks'
TEST_DIR = 'tests'
BLACKLIST = [
    '__init__',
    '.pyc'
]

def _filter(_list):
    return [x for x in _list if re.search(r'__init__|.pyc', x) is None]

if __name__ == '__main__':
    tasks = _filter(os.listdir(TASK_DIR))
    tests = [x.replace('test_', '') for x in _filter(os.listdir(TEST_DIR))]

    ldiff = [x for x in tasks if x not in tests]

    print('COUNT: {0}'.format(len(ldiff)))
    [print('--> {0}'.format(x)) for x in ldiff]
