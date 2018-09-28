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
#                   cache
#                   encoding
#
# Imports
# ------------------------------------------------------------------------ 79->
from transport.cache import Cache  # pragma: no cover

from common.encoding cimport Tools
import time

cimport cython
from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.list cimport list as clist
from libcpp.utility cimport pair
from libcpp.string cimport string
from libcpp.map cimport map
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast8_t, uint_fast16_t
from libc.stdint cimport int_fast16_t
from libc.stdio cimport printf
from libc.stdlib cimport atoi
from posix cimport time as p_time
from libcpp.typeinfo cimport type_info
from cython.operator cimport typeid
#import numpy as np
cimport numpy as np


# Globals
# ------------------------------------------------------------------------ 79->
cdef struct Meta:
    unsigned long length
    unsigned long lifespan
    string cache_key
    string spent_key

cdef Tools TOOLS = Tools()

cdef struct Pipeline:
    clist[string] tasks
    clist[string] completed
    unordered_map[string, string] kwargs

ctypedef pair[unordered_map[string, clist[string]], unordered_map[string, string]] Pipe
ctypedef pair[unordered_map[string, string], vector[vector[double]]] Segment
ctypedef vector[Segment] Data
cdef string VERSION = version()

cdef public Data dataframe

# Classes
# ------------------------------------------------------------------------ 79->

cdef class Parcel:
    cpdef pack(self, route, envelope)
    cpdef unpack(self)
    cpdef load(self, parcel)
    cpdef seal(self)

cdef class Container:
    cdef:
        public np.ndarray header
        public dict meta
        public string data
        public vector[string] manifest
        public bint unseal
        public string sealed_meta
        public list sealed_buffer
    '''
    cdef int_fast16_t _set(self, char* key, string value) except -1
    cdef bint _has(self, vector[string] v, string key)
    cdef bint _compression(Container self)
    cdef object _flatten(Container self, object obj)
    cdef object _compress(Container self, object obj)
    '''

cdef class Envelope:
    cdef:
        public np.ndarray header
        public dict meta
        public string data
        public vector[string] manifest
        public bint unseal
        public string sealed_meta
        public list sealed_buffer

    cpdef list open(self, bint compressed=?)
    cpdef void pack(self, dict meta, list data)
    cdef void load(self, list sealed_envelope, bint unseal=?)
    cdef list seal(self)
    cdef void update_header(self)
    cdef void consume(self)
    cdef long get_lifespan(self)
    cdef long get_length(self)
    cdef string get_header(self)
    cdef string get_sealed_data(self)
    cdef np.ndarray get_data(self)
    cdef long get_shape(self)
    cdef void set_data(self, np.ndarray data)
    cpdef np.ndarray result(self)

# Functions
# ------------------------------------------------------------------------ 79->

cdef string version()
cdef np.ndarray init_meta()
cdef Pipeline init_pipeline()
cdef Data init_data()
cdef Pipeline map_to_pipeline(dict _dict)
cdef np.ndarray map_to_meta(dict _dict)
cdef Data map_to_data(list _list)
cdef list get_datatypes(dict _dict)

cpdef list dataFrame3(list l, dict d)
cpdef np.ndarray dataFrame(object obj, tuple shape, object dtype)
cdef np.ndarray list_to_ndarray(list obj, type dtype, tuple shape)
cdef np.ndarray map_to_ndarray(dict obj, list dtype)

# Main
# ------------------------------------------------------------------------ 79->
