import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.subtract import task_subtract
from dummy_data import KWARGS, CONTENTS

def test_subtract():
    KWARGS = {
        'operations': [
            {
                'a': 'a',
                'b': 'b',
                'column': 'c1'
            },
            {
                'a': 'a',
                'b': 1,
                'column': 'c2'
            }
        ]
    }
    r = task_subtract(KWARGS, CONTENTS)
    assert r['c1'][2] == 0
    assert r['c2'][2] == 3.0
