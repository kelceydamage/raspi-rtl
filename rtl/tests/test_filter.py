from rtl.tasks.filter import task_filter
from dummy_data import KWARGS, CONTENTS2

def test_filter():
    KWARGS = {
        'operations': [
            {
            'column': 'a',
            'value': 2,
            'method': 'eq'
            },
            {
            'column': 'a',
            'value': 2,
            'method': 'ne'
            },
        ]
    }
    r = task_filter(KWARGS, CONTENTS2)
    KWARGS = {
        'operations': [
            {
            'column': 'a',
            'value': 2,
            'method': 'lt'
            },
            {
            'column': 'a',
            'value': 2,
            'method': 'le'
            },
        ]
    }
    r = task_filter(KWARGS, CONTENTS2)
    KWARGS = {
        'operations': [
            {
            'column': 'a',
            'value': 2,
            'method': 'gt'
            },
            {
            'column': 'a',
            'value': 2,
            'method': 'ge'
            }
        ]
    }
    r = task_filter(KWARGS, CONTENTS2)
    assert r['a'][0] == 0
