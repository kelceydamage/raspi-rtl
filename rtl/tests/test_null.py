from rtl.tasks.null import task_null
from dummy_data import KWARGS, CONTENTS2

def test_null():
    r = task_null(KWARGS, CONTENTS2)
    assert r['a'][2] == 2
