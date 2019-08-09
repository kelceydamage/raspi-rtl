import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from rtl.tasks.normalize import task_normalize
from dummy_data import KWARGS, CONTENTS3

def test_normalize():
    KWARGS = {
        'columns': [
            'a',
            'b'
        ],
        'model': 'DistanceFromMean',
        'weight': 0.01
    }
    r = task_normalize(KWARGS, CONTENTS3)
    assert r['bNormal'][2] == 10
    assert r['aNormal'][0] == 0