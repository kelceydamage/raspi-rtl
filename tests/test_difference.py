import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.difference import task_difference
from dummy_data import KWARGS, CONTENTS2

def test_difference():
    KWARGS['task_difference'] = {
        'operations': [
            {
                'a': 'a',
                'b': 'b',
                'column': 'c'
            }
        ]
    }
    r = task_difference(KWARGS, CONTENTS2)
    assert r['ndata']['a'][2] == 2
