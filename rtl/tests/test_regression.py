import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from rtl.tasks.regression import task_regression
from dummy_data import KWARGS, CONTENTS3

def test_linear_regression():
    KWARGS = {
        'operations': [
            {
                'x': 'a',
                'y': 'b',
                'space': 'linear',
                'model': 'Linear'
            },
        ]
    }
    r = task_regression(KWARGS, CONTENTS3)
    assert r['bLinear'].tolist() == [
        10.500000000000002, 11.000000000000002, 11.5, 12.0
    ]

def test_poly_regression():
    KWARGS = {
        'operations': [
            {
                'x': 'a',
                'y': 'b',
                'space': 'linear',
                'model': 'Poly',
                'd': 3
            },
        ]
    }
    r = task_regression(KWARGS, CONTENTS3)
    assert r['bPoly'].tolist() == [
        2.000000000000078, 23.000000000000068, 13.000000000000064, 7.000000000000071
    ]
    #[2.000000000000078, 23.000000000000046, 13.000000000000021, 6.999999999999964]
    # Precision is system dependant and often this test will fail.
