#! /usr/bin/env python
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from rtl.common.transform import Transform

DSDSL = {
    0: {
        'tasks': {
            'task_null': {}
        }
    }
}

if __name__ == '__main__':
    Job = Transform().execute(DSDSL).result()