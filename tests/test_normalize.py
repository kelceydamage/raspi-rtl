import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.normalize import task_normalize
from dummy_data import KWARGS, CONTENTS3

def test_normalize():
    KWARGS['task_normalize'] = {
        'columns': [
            'a',
            'b'
        ],
        'model': 'DistanceFromMean',
        'weight': 0.01
    }
    r = task_normalize(KWARGS, CONTENTS3)
    assert r['ndata']['bNormal'][2] == 11.040422222222224
    assert r['ndata']['aNormal'][0] == 0
