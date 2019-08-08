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
#                   zmq
#                   common
#                   conf
#
# Imports
# ------------------------------------------------------------------------ 79->

# Cython imports
cimport cython
from common.datatypes cimport Envelope

# Globals
# ------------------------------------------------------------------------ 79->

VERSION = '2.0a'

# Classes
# ------------------------------------------------------------------------ 79->


cdef class Dispatcher:
    cdef:
        object push_socket
        object sub_socket
        list results

    # Python acccessible API
    cpdef Envelope send(self, Envelope envelope)

    # CPP/Cython acccessible API
    cdef Envelope _recieve(self)
    cdef void close(self)
    cdef Envelope _send(self, Envelope envelope)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
