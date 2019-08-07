#!python
#cython: language_level=3, cdivision=True
###boundscheck=False, wraparound=False //(Disabled by default)
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

import time
from common.print_helpers import printc, Colours, print_stage
from common.decorators import timer

from common.datatypes cimport Envelope
from transport.dispatch cimport Dispatcher


# ------------------------------------------------------------------------ 79->
COLOURS = Colours()

"""
'contents': {
            'data': None,
            'ndata': self.envelope.raw_ndata().tolist(),
            'dtypes': self.envelope.raw_dtypes()
        },
"""

# Classes
# ------------------------------------------------------------------------ 79->
cdef class Transform:
    cdef:
        Dispatcher dispatcher
        Envelope envelope

    def __init__(self):
        self.dispatcher = Dispatcher()
        self.envelope = Envelope(cached=False)

    cdef void run(self, long i):
        printc(
            'Running: {0} - {1}'.format(i, self.envelope.header[0][0]), 
            COLOURS.PURPLE
        )
        self.envelope = self.dispatcher.send(self.envelope)

    cdef void validateSchema(self, dict schema):
        if 'tasks' not in schema.keys():
            printc('FAIL: missing key: {0} in schema'.format('tasks'), COLOURS.RED)
            exit(1)
        if schema['tasks'] is None or not isinstance(schema['tasks'], dict):
            printc('FAIL: missing/malformed task dict in schema', COLOURS.RED)
            exit(0)

    cdef void setup(self, dict schema):
        self.validateSchema(schema)

    cdef void pack(self, dict stage, long id):
        cdef:
            dict content

        if id == 0:
            content = self.envelope.get_contents()
            content['ndata'] = None
            self.envelope.pack(
                meta={
                    'tasks': list(stage['tasks'].keys()),
                    'completed': [],
                    'kwargs': stage['tasks']
                },
                contents=content
            )
        else:
            self.envelope.modify_meta(
                meta={
                    'tasks': list(stage['tasks'].keys()),
                    'completed': [],
                    'kwargs': stage['tasks']
                }
            )

    cpdef Envelope execute(self, dict dsdsl):
        cdef:
            long i
            long l = len(dsdsl.keys())

        start = time.perf_counter()
        for i in range(l):
            self.setup(dsdsl[i])
            self.pack(dsdsl[i], i)
            t = time.perf_counter()
            self.run(i)
            print('RUNTIME', time.perf_counter() - t)
        elapsed = time.perf_counter() - start
        print('Total Elapsed Time:', elapsed)
        return self.envelope


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->