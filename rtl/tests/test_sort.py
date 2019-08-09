import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from rtl.tasks.sort import task_sort
from dummy_data import KWARGS, CONTENTS2

def test_sort():
    KWARGS= {
        'axis': 0,
        'method': 'quicksort',
        'column': 'b'
    }
    r = task_sort(KWARGS, CONTENTS2)
    assert r['a'][2] == 1
