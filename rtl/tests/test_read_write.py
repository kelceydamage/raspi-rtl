from rtl.tasks.open_array import task_open_array
from rtl.tasks.write import task_write
from dummy_data import KWARGS, CONTENTS

def test_read_write():
    KWARGS = {
        'filename': 'test',
        'path': 'raw_data',
        'extension': 'csv',
        'delimiter': ','
    }
    KWARGS = {
        'filename': 'test',
        'path': 'raw_data',
        'extension': 'csv',
        'delimiter': ','
    }
    # r = task_write(KWARGS, CONTENTS)
    # Only works locally and not in CI, as it requires the file 
    # created by the above call.
    # r = task_open_array(KWARGS, CONTENTS)
    # assert r['ndata']['a'][3] == 4
