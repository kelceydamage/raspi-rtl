import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from rtl.tasks.multiply import task_multiply
from dummy_data import KWARGS, CONTENTS

def test_multiply():
    KWARGS = {
        'operations': [
            {
                'a': 'a',
                'b': 'b',
                'column': 'c1'
            },
            {
                'a': 'a',
                'b': 2,
                'column': 'c2'
            }
        ]
    }
    r = task_multiply(KWARGS, CONTENTS)
    assert r['c1'][2] == 16
    assert r['c2'][2] == 8
