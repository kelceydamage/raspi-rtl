import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.square_root import task_square_root
from dummy_data import KWARGS, CONTENTS3

def test_square_root():
    KWARGS['task_square_root'] = {
        'operations': [
            {
                'a': 'b',
                'column': 'c'
            }
        ]
    }
    r = task_square_root(KWARGS, CONTENTS3)
    assert r['ndata']['c'][2] == 3.605551275463989
