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
import cbor
from libcpp.string cimport string
from common.print_helpers import printc, Colours, print_stage
from common.decorators import timer
from transport.cache import ExperimentalCache
from transport.conf.configuration import DEBUG

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
        object cache

    def __init__(self):
        self.dispatcher = Dispatcher()
        self.envelope = Envelope(cached=False)
        self.cache = ExperimentalCache()

    cdef void run(self, long i):
        if DEBUG: print('TRANSFORM: run')
        printc(
            'Running: {0} - {1}'.format(i, self.envelope.getId()), 
            COLOURS.PURPLE
        )
        self.envelope = self.dispatcher.send(self.envelope)

    cdef void validateSchema(self, dict schema):
        if DEBUG: print('TRANSFORM: validateSchema')
        if 'tasks' not in schema.keys():
            printc('FAIL: missing key: {0} in schema'.format('tasks'), COLOURS.RED)
            exit(1)
        if schema['tasks'] is None or not isinstance(schema['tasks'], dict):
            printc('FAIL: missing/malformed task dict in schema', COLOURS.RED)
            exit(0)

    cdef void storeSchema(self, dict schema, bytes _id):
        if DEBUG: print('TRANSFORM: storeSchema')
        self.cache.put(_id, cbor.dumps(schema['tasks']))

    cdef void setup(self, dict schema, bytes _id):
        if DEBUG: print('TRANSFORM: setup')
        self.validateSchema(schema)
        self.storeSchema(schema, _id)
        
    cdef void pack(self, dict schema, long id):
        if DEBUG: print('TRANSFORM: pack')
        if id == 0:
            self.envelope.pack(1)
        else:
            self.envelope.createId()
            self.envelope.setLifespan(1)
        self.setup(schema, self.envelope.getId())
        
    cpdef Envelope execute(self, dict dsdsl):
        if DEBUG: print('TRANSFORM: execute')
        cdef:
            long i
            long l = len(dsdsl.keys())

        start = time.perf_counter()
        for i in range(l):
            self.pack(dsdsl[i], i)
            self.run(i)
        elapsed = time.perf_counter() - start
        print('Total Elapsed Time:', elapsed)
        return self.envelope


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->