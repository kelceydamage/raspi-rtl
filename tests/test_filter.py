import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.filter import task_filter
from dummy_data import KWARGS, CONTENTS2

def test_filter():
    KWARGS['task_filter'] = {
        'operations': [
            {
            'column': 'a',
            'value': 2,
            'method': 'eq'
            }
        ]
    }
    r = task_filter(KWARGS, CONTENTS2)
    print(r)
    assert r['ndata']['a'][0] == 2