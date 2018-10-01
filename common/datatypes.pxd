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
#                   numpy
#                   libcpp.string
#
# Imports
# ------------------------------------------------------------------------ 79->

cimport cython
from numpy cimport ndarray
from libcpp.string cimport string

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->

cdef class Envelope:
    cdef:
        public string version
        public ndarray header
        public dict meta
        public string data
        public bint unseal
        public string sealed_meta
        public list sealed_buffer
        public list meta_dtypes

    # Python accessible API
    cpdef ndarray result(self)
    cpdef void pack(self, dict meta, list data)

    # CPP/Cython acccessible API
    cdef string create_id(self)
    cdef void load(self, list sealed_envelope, bint unseal=?)
    cdef list seal(self)
    cdef void consume(self)
    cdef long get_shape(self)
    cdef long get_lifespan(self)
    cdef long get_length(self)
    cdef string get_header(self)
    cdef string get_sealed_data(self)
    cdef ndarray get_data(self)
    cdef void set_data(self, ndarray data)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
