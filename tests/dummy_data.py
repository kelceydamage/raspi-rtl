import numpy as np

DTYPE = [('a', '<i8'), ('b', '<i8')]
NDATA = np.ones((4), dtype=DTYPE)
NDATA['a'].fill(4)
NDATA['b'].fill(4)
NDATA2 = np.ones((4), dtype=DTYPE)
NDATA2['a'] = np.arange(4)
NDATA2['b'] = np.arange(4)[::-1]
NDATA3 = np.ones((4), dtype=DTYPE)
NDATA3['a'] = np.arange(4)
NDATA3['b'] = [2, 23, 13, 7]

KWARGS = {}
CONTENTS = {
    'data': {},
    'ndata': NDATA,
    'dtypes': DTYPE,
    'reduces': {}
}

CONTENTS2 = {
    'data': {},
    'ndata': NDATA2,
    'dtypes': DTYPE,
    'reduces': {}
}

CONTENTS3 = {
    'data': {},
    'ndata': NDATA3,
    'dtypes': DTYPE,
    'reduces': {}
}
