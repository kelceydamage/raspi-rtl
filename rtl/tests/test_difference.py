import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from rtl.tasks.difference import task_difference
from dummy_data import KWARGS, CONTENTS2

def test_difference():
    KWARGS = {
        'operations': [
            {
                'a': 'a',
                'b': 'b',
                'column': 'c'
            }
        ]
    }
    r = task_difference(KWARGS, CONTENTS2)
    assert r['a'][2] == 2
