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
    KWARGS['task_subtract'] = {
        'operations': [
            {
                'a': 'a',
                'b': 'b',
                'column': 'c'
            }
        ]
    }
    r = task_subtract(KWARGS, CONTENTS)
    assert r['ndata']['c'][2] == 0
