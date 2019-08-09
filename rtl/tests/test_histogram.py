import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from rtl.tasks.histogram import task_histogram
from dummy_data import KWARGS, CONTENTS2

def test_histogram():
    KWARGS = {
        'operations': [
            {
                'a': 'a',
                'bins': 2,
                'column': 'c1'
            }
        ]
    }
    r = task_histogram(KWARGS, CONTENTS2)
    assert r['c1'][1] == 1.5