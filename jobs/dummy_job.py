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
from common.print_helpers import printc, Colours
from transport.cache import Cache
import time
import numpy as np
import cbor
import io

# Globals
# ------------------------------------------------------------------------ 79->
COLOURS = Colours()
COUNT = 5

# Classes
# ------------------------------------------------------------------------ 79->


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    loop = COUNT

    dispatcher = Dispatcher()

    envelope = datatypes.Envelope(cached=False)

    tasks = ['task_multiply', 'task_multiply', 'task_multiply', 'task_multiply']

    data = [[1.0, 2.0, 3.0] for i in range(loop)]

    envelope.pack(meta={'tasks': tasks, 'completed': [], 'kwargs': {}}, data=data)

    print('Start Job')

    #print(envelope.result())

    t4 = time.perf_counter()
    envelope = dispatcher.send(envelope)

    printc('JOB COMPLETED: {0}s'.format(time.perf_counter() - t4), COLOURS.GREEN)


    print(envelope.header)
    print('-'*79)

    print('JOB', envelope.result()[:10])
    print(envelope.header)

