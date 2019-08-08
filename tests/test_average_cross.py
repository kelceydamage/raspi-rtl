import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.average_cross import task_average_cross
from dummy_data import KWARGS, CONTENTS3

def test_average_cross():
    KWARGS = {
        'operations': [
            {
                'column': 'c',
                'columns': [
                    'a',
                    'b'
                ]
            }
        ]
    }
    r = task_average_cross(KWARGS, CONTENTS3)
    assert r['c'][2] == 7.5
