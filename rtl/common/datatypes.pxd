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
from cpython cimport Py_buffer
from numpy cimport ndarray
from numpy cimport dtype
from libcpp.string cimport string

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->

cdef class Envelope:
    cdef:
        public string version
        list sealed_buffer
        object dtypes
        long lifespan
        long length
        long width
        string id
        object ndataBuffer
        ndarray ndata

    # Python accessible API
    cpdef ndarray result(self)
    cpdef void pack(self, long lifespan, list dtypes=?, ndarray ndata=?)

    # CPP/Cython acccessible API
    cdef void load(self, list sealed_envelope)
    cdef list seal(self)
    cdef string getId(self)
    cdef void createId(self)
    cdef long getLength(self)
    cdef long getWidth(self)
    cdef long getLifespan(self)
    cdef void setLifespan(self, long i)
    cdef dtype getDtypes(self)
    cdef ndarray getContents(self)
    cdef void setContents(self, ndarray ndata)
    cdef void consume(self)


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
