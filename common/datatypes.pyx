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

# Python imports
import cbor
from uuid import uuid4
from numpy import array, frombuffer

# Cython imports
cimport cython
from numpy cimport ndarray
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
    """.format(VERSION)

    __slots__ = [
        'header',
        'meta',
        'data',
        'ndata',
        'cached',
        'compressed',
        'cache',
        'length',
        'lifespan',
        'tools'
        ]

    def __cinit__(self):
        self.version = VERSION.encode()
        self.meta_dtypes = [
            ('id', 'a70'), 
            ('lifespan', 'i4'), 
            ('length', 'i4'),
            ('shape', 'i4')
            ]

    cpdef ndarray result(self):
        return self.get_ndata()

    # ndata is numeric types of fixed length that can be compressed into ndarrays.
    cpdef void pack(self, dict meta={}, list ndata=[[]], dict data={'d': 'x01'}):
        cdef string _id = self.create_id()
        cdef ndarray h = ndarray(
            (1,), 
            dtype=self.meta_dtypes
            )
        self.header = h
        self.header['id'] = _id
        self.header['lifespan'] = len(meta['tasks'])
        self.header['length'] = len(ndata)
        self.header['shape'] = len(ndata[0])
        self.meta = meta
        self.ndata = ndarray(
            (self.header['length'][0], (self.header['shape'][0])), 
            buffer=array(ndata)
            ).tobytes()
        self.data = data
        self.unseal = True

    cdef string create_id(self):
        return <string>str(uuid4()).encode()

    cdef void load(self, list sealed_envelope, bint unseal=False):
        self.unseal = unseal
        self.header = frombuffer(
            sealed_envelope[0], 
            dtype=self.meta_dtypes
            ).reshape(1, )
        self.header.setflags(write=1)
        self.ndata = <string>sealed_envelope[2]
        if self.unseal:
            self.meta = cbor.loads(sealed_envelope[1])
            self.data = cbor.loads(sealed_envelope[3])
        else:
            self.sealed_meta = sealed_envelope[1]
            self.sealed_data = sealed_envelope[3]

    cdef list seal(self):
        cdef: 
            string m = <string>cbor.dumps(self.meta)
            string d = <string>cbor.dumps(self.data)
            string h = <string>self.header.tobytes()
            list l
        if self.unseal:
            l = [h, m, self.ndata, d]
            return l
        l = [self.header.tobytes(), self.sealed_meta, self.ndata, self.sealed_data]
        return l

    cdef void consume(self):
        self.meta['completed'].append(self.meta['tasks'].pop(0))
        self.header['lifespan'][0] -= 1

    cdef long get_shape(self):
        return self.header['shape'][0]

    cdef long get_lifespan(self):
        return self.header['lifespan'][0]

    cdef long get_length(self):
        return self.header['length'][0]

    cdef string get_header(self):
        return self.header['id'][0]
    
    cdef string get_sealed_data(self):
        return self.ndata

    cdef dict get_data(self):
        return <dict>self.data

    cdef void set_data(self, data):
        self.data = data

    cdef ndarray get_ndata(self):
        return frombuffer(self.ndata).reshape(
            self.get_length(), 
            self.get_shape()
            )

    cdef void set_ndata(self, ndarray data):
        self.header['length'] = len(data)
        self.header['shape'] = len(data[0])
        self.ndata = data.tobytes()

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
