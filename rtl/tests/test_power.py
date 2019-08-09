import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from rtl.tasks.power import task_power
from dummy_data import KWARGS, CONTENTS3

def test_power():
    KWARGS = {
        'operations': [
            {
                'a': 'b',
                'b': 2,
                'column': 'c'
            }
        ]
    }
    r = task_power(KWARGS, CONTENTS3)
    assert r['c'][2] == 169.0
