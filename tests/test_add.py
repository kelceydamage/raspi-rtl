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
    KWARGS['task_add'] = {
        'operations': [
            {
                'a': 'a',
                'b': 'b',
                'column': 'c'
            }
        ]
    }
    r = task_add(KWARGS, CONTENTS)
    assert r['ndata']['c'][2] == 8
