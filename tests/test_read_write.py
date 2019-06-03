import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from tasks.open_array import task_open_array
from tasks.write import task_write
from dummy_data import KWARGS, CONTENTS

def test_read_write():
    KWARGS['task_write'] = {
        'filename': 'test',
        'path': 'raw_data',
        'extension': 'csv',
        'delimiter': ','
    }
    KWARGS['task_open_array'] = {
        'filename': 'test',
        'path': 'raw_data',
        'extension': 'csv',
        'delimiter': ','
    }
    r = task_write(KWARGS, CONTENTS)
    r = task_open_array(KWARGS, CONTENTS)
    print(r)
    assert r['ndata']['a'][3] == 4
