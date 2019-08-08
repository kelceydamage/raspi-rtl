import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.log import task_log
from dummy_data import KWARGS, CONTENTS3

def test_log():
    KWARGS = {
        'operations': [
            {
                'a': 'b',
                'column': 'c'
            }
        ]
    }
    r = task_log(KWARGS, CONTENTS3)
    assert r['c'][2] == 2.5649493574615367
