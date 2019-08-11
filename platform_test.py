#! /usr/bin/env python
"""Run a basic test on RTL to ensure it works"""
from rtl.common.transform import Transform

DSDSL = {
    0: {
        'tasks': {
            'null': {}
        }
    }
}

if __name__ == '__main__':
    JOB = Transform().execute(DSDSL).result()
