from rtl.tasks.square_root import task_square_root
from dummy_data import KWARGS, CONTENTS3

def test_square_root():
    KWARGS = {
        'operations': [
            {
                'a': 'b',
                'column': 'c'
            }
        ]
    }
    r = task_square_root(KWARGS, CONTENTS3)
    assert r['c'][2] == 3.605551275463989
