import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.simple_plot import task_simple_plot
from web.plot import PLOT_QUEUE
from dummy_data import KWARGS, CONTENTS

def test_plot():
    KWARGS['task_simple_plot'] = {
        'plots': {
            'test': [
                {
                    'x': 'a',
                    'y': 'b',
                    'type': 'circle',
                    'scale': 'linear',
                    'series': None
                }
            ]
        }
    }
    r = task_simple_plot(KWARGS, CONTENTS)
    q = PLOT_QUEUE.get()
    assert q['draws'][0]['x'][0] == 4
