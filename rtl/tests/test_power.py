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
    KWARGS = {
        'operations': [
            {
                'a': 'b',
                'b': 'a',
                'column': 'c'
            }
        ]
    }
    r = task_power(KWARGS, CONTENTS3)
    assert r['c'][2] == 169.0
