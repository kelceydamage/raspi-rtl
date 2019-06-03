import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.divide import task_divide
from dummy_data import KWARGS, CONTENTS

def test_divide():
    KWARGS['task_divide'] = {
        'operations': [
            {
                'a': 'a',
                'b': 'b',
                'column': 'c'
            }
        ]
    }
    r = task_divide(KWARGS, CONTENTS)
    assert r['ndata']['c'][2] == 1
