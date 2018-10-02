#!/usr/bin/env python3
# ------------------------------------------------------------------------ 79->
# Author: ${name=Kelcey Damage}
# Python: 3.5+
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Doc
# ------------------------------------------------------------------------ 79->

# Imports
# ------------------------------------------------------------------------ 79->
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
import zmq
from transport.dispatch import Dispatcher
from common import datatypes
from common.print_helpers import *
from transport.cache import Cache
import time
import numpy as np
import cbor
import io

# Globals
# ------------------------------------------------------------------------ 79->
COLOURS = Colours()
COUNT = 500000
CACHE = Cache()

# Classes
# ------------------------------------------------------------------------ 79->


# Functions
# ------------------------------------------------------------------------ 79->
def map_to_meta(_dict):
    t = time.perf_counter()
    datatypes = [(x[0].decode(), 'a8') for x in list(_dict.items())]
    m = np.fromiter(
        _dict.items(),
        dtype=datatypes,
        count=len(_dict)
        )
    print('{0:.8f}'.format(time.perf_counter() - t))
    print(m.shape)
    return datatypes

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    loop = COUNT
    seed = [[1.0, 2.0, 3.0] for x in range(loop)]
    seed2 = {b'foo': b'bar', b'baz': b'bar'}
    k = map_to_meta(seed2)
    s = time.time()
    dispatcher = Dispatcher()
    print('_'*79)
    pipeline = {}

    envelope = datatypes.Envelope(cached=False)
    tasks = ['task_multiply', 'task_multiply', 'task_multiply', 'task_multiply']
    data = [[1.0, 2.0, 3.0] for i in range(loop)]
    #t = time.perf_counter()
    envelope.pack(meta={'tasks': tasks, 'completed': [], 'kwargs': {}}, data=data)
    #print('PACK {0:.8f}'.format(time.perf_counter() - t))

    print('Start Job')
    t4 = time.perf_counter()
    envelope = dispatcher.send(envelope)
    printc('JOB COMPLETED: {0}s'.format(time.perf_counter() - t4), COLOURS.GREEN)


    print(envelope.header)
    print('-'*79)
    r = []
    data = envelope.result()
    data.setflags(write=1)
    t1 = time.perf_counter()
    for i in range(len(tasks)):
        for i in range(data.shape[0]):
            data[i] = np.multiply(data[i], data[i])
    print('CTRL w/ PyWrap\t {0:.8f}'.format(time.perf_counter() - t1))

    print('JOB', envelope.result()[:10])
    print(envelope.header)

