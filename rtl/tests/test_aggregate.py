import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from rtl.tasks.aggregate import task_aggregate
from dummy_data import KWARGS, CONTENTS3

def test_aggregate():
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
    r = task_aggregate(KWARGS, CONTENTS3)
    assert r['c'][2] == 7.5