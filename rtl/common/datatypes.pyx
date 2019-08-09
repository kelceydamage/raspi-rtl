#!python
#cython: language_level=3, cdivision=True
###boundscheck=False, wraparound=False //(Disabled by default)
# ------------------------------------------------------------------------ 79->
# Author: Kelcey Damage
# Cython: 0.28+
# Doc
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
# Dependancies:
#                   cython
#                   cbor
#                   numpy
#                   uuid.uuid4
#                   libcpp.string
#
# Imports
# ------------------------------------------------------------------------ 79->
DEF GPU = 0

# Python imports
import cbor
from uuid import uuid4
from ast import literal_eval
from array import array as parray
import time
IF GPU == 1:
    from cupy import array
    from numpy import frombuffer, dtype
ELSE:
    print('Failed to load CuPy falling back to Numpy')
    from numpy import array, frombuffer, dtype
from rtl.transport.conf.configuration import DEBUG
#from numpy import array, frombuffer, dtype

# Cython imports
cimport cython
from numpy cimport ndarray
from numpy cimport dtype
from libcpp.string cimport string

# Globals
# ------------------------------------------------------------------------ 79->

VERSION = '2.0a'

# Classes
# ------------------------------------------------------------------------ 79->

cdef class Envelope:
    """
    NAME:           Envelop {0}

    DESCRIPTION:    The primary object for housing and transmitting request 
                    on RTL.

    METHODS:        .result()
                    Python interface for retrieving the data as an ndarray of 
                    ndarrays.

                    .pack(meta, data)
                    Packs up a dict of meta attributes and a list of data 
                    arrays into and envelope(obj).

                    .load(sealed_envelope)
                    Loads an encoded list of bytes into an envelope.

                    .seal()
                    Returns the content as a list of bytes objects for
                    transmission.

                    .consume()
                    Moves the current task into the completed array. Used for 
                    tracking and decrementing lifespan.

                    .get_shape()
                    Returns the second dimension size of the data payload.

                    .get_lifespan()
                    Returns the envelopes lifespan in terms of remaining 
                    tasks to complete.

                    .get_length()
                    Returns the amount of sub arrays in the data payload.

                    .get_header()
                    Returns the envelopes id as a bytestring.

                    .get_sealed_data()
                    Returns the envelopes data as bytes.

                    .get_data()
                    Returns the envelopes bytes data as an ndarray of ndarrays.

                    .set_data(data)
                    Takes an ndarray and converts to a bytes object, while 
                    updating both the envelopes length and shape attributes.

    [id, lifespan, length, width, dtypes, ndarray]

    """.format(VERSION)

    def __cinit__(self):
        self.version = VERSION.encode()

    cpdef void pack(self, long lifespan, list dtypes=None, ndarray ndata=None):
        if DEBUG: print('ENVELOPE: pack')
        if dtypes == None:
            dtypes = [(str(1), '<i8')]
        if ndata == None:
            try:
                ndata = ndarray((1, ), buffer=array([[0], [0]]), dtype=dtype(dtypes))
            except Exception as e: print(e)
        self.createId()
        self.lifespan = lifespan
        self.dtypes = memoryview(cbor.dumps(str(dtypes)))
        self.ndata = ndata
        self.length = self.ndata.shape[0]
        self.width = self.ndata.shape[1]

    cdef list seal(self):
        if DEBUG: print('ENVELOPE: seal')
        cdef:
            object contents

        if self.ndata is None:
            contents = self.ndataBuffer
        else:
            contents = self.ndata
        return [
            self.id,
            <string>cbor.dumps(self.lifespan),
            <string>cbor.dumps(self.length),
            <string>cbor.dumps(self.width),
            self.dtypes,
            contents
        ]

    cdef void load(self, list sealed_envelope):
        if DEBUG: print('ENVELOPE: load')
        try:
            self.id = sealed_envelope[0].bytes
            self.lifespan = cbor.loads(sealed_envelope[1].bytes)
            self.length = cbor.loads(sealed_envelope[2].bytes)
            self.width = cbor.loads(sealed_envelope[3].bytes)
            self.dtypes = sealed_envelope[4] #dtype(literal_eval(cbor.loads(sealed_envelope[4].bytes)))
            self.ndataBuffer = sealed_envelope[5]
        except Exception as e: print('LOAD', e)

    cdef void createId(self):
        if DEBUG: print('ENVELOPE: create_id')
        self.id = <string>str(uuid4()).encode('utf-8')

    cdef string getId(self):
        return self.id

    cdef long getLength(self):
        return self.length

    cdef long getWidth(self):
        return self.width

    cdef long getLifespan(self):
        return self.lifespan

    cdef void setLifespan(self, long i):
        self.lifespan = i

    cdef dtype getDtypes(self):
        return dtype(literal_eval(cbor.loads(self.dtypes.bytes)))

    cdef ndarray getContents(self):
        if DEBUG: print('ENVELOPE: getContents')
        return frombuffer(
            memoryview(self.ndataBuffer),
            dtype=self.getDtypes()
        )

    cdef void setContents(self, ndarray ndata):
        if DEBUG: print('ENVELOPE: setContents')
        self.ndata = ndata
        self.dtypes = memoryview(cbor.dumps(str(self.ndata.dtype)))
        self.length = self.ndata.shape[0]
        self.width = self.ndata.shape[1]

    cdef void consume(self):
        self.lifespan -= 1

    cpdef ndarray result(self):
        return self.getContents()


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
