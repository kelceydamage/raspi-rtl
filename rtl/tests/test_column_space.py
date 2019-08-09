from rtl.tasks.column_space import task_column_space
from dummy_data import KWARGS, CONTENTS3

def test_column_space():
    KWARGS = {
        'column': 'b',
        'space': 'linear',
    }
    r = task_column_space(KWARGS, CONTENTS3)
    assert r['bSpace'][2] == 15
