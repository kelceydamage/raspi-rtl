import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.column_space import task_column_space
from dummy_data import KWARGS, CONTENTS3

def test_column_space():
    KWARGS = {
        'column': 'b',
        'space': 'linear',
    }
    r = task_column_space(KWARGS, CONTENTS3)
    assert r['bSpace'][2] == 15
