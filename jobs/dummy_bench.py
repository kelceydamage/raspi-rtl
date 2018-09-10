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
from common.datatypes import *
from common.print_helpers import *
from transport.cache import Cache
import time

# Globals
# ------------------------------------------------------------------------ 79->
COLOURS = Colours()
COUNT = 2
CACHE = Cache()

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    s = time.time()
    dispatcher = Dispatcher()
    pipeline = PIPELINE
    data = [[1, 2, 3] for i in range(500000)]
    envelope = Envelope(cached=False)
    pipeline['tasks'] = ['task_sum', 'task_sum', 'task_sum', 'task_sum']
    envelope.pack(pipeline=pipeline, data=data)
    print('Envelope Length:', envelope.length)
    envelope = dispatcher.send(envelope)

    printc('JOB COMPLETED: {0}s'.format(time.time() - s), COLOURS.GREEN)
    # Serial bench
    s = time.time()
    
    results = []
    for item in data:
        l = sum(item)
        results.append([l])
    print(time.time() - s)
    s = time.time()
    r = []

    while data:
        r.append([sum(data.pop())])
    print(time.time() - s)


    printc('{0} Sums took: {1}'.format(len(r), time.time() - s), COLOURS.GREEN)

