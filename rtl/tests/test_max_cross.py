import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from rtl.tasks.max_cross import task_max_cross
from dummy_data import KWARGS, CONTENTS

def test_max_cross():
    KWARGS = {
        'operations': [
            {
                'columns': ['a', 'b'],
                'column': 'c1'
            }
        ]
    }
    r = task_max_cross(KWARGS, CONTENTS)
    assert r['c1'][2] == 4.0
