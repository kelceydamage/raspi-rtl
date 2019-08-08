import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.add import task_add
from dummy_data import KWARGS, CONTENTS

def test_add():
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
    r = task_add(KWARGS, CONTENTS)
    assert r['c1'][2] == 8
    assert r['c2'][2] == 5.0
