from rtl.tasks.average import task_average
from dummy_data import KWARGS, CONTENTS3

def test_average():
    KWARGS = {
        'operations': [
            {
                'a': 'b',
                'column': 'c'
            }
        ]
    }
    r = task_average(KWARGS, CONTENTS3)
    assert r['c'][2] == 11.25
