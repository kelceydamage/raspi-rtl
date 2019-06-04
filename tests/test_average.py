import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.average import task_average
from dummy_data import KWARGS, CONTENTS3

def test_average():
    KWARGS['task_average'] = {
        'operations': [
            {
                'a': 'b',
                'column': 'c'
            }
        ]
    }
    r = task_average(KWARGS, CONTENTS3)
    assert r['ndata']['c'][2] == 11.25
