import numpy as np

DTYPE = [('a', '<i8'), ('b', '<i8')]
NDATA = np.ones((4), dtype=DTYPE)
NDATA['a'].fill(4)
NDATA['b'].fill(4)
KWARGS = {}
CONTENTS = {
    'data': {},
    'ndata': NDATA,
    'dtypes': DTYPE,
    'reduces': {}
}