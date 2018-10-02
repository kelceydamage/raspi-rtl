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
#                   conf
#                   common
#                   zmq
#
# Imports
# ------------------------------------------------------------------------ 79->

# Cython imports
cimport cython
from numpy cimport ndarray
from common.datatypes cimport Envelope
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast16_t

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->


cdef class Relay:
    cdef:
        uint_fast16_t pid
        long chunk_size
        list chunk_buffer
        bint success
        dict assembly_buffer
        unordered_map[string, long] state
        object recv_socket
        object send_socket
        object publisher
        Envelope envelope
        dict index_tracker
        ndarray chunk_holder
        string version

    # Python accessible API
    cpdef void start(self)

    # CPP/Cython acccessible API
    cdef void send(self)
    cdef void publish(self)
    cdef void recv_loop(self)
    cdef void create_state(self, string header, long length)
    cdef long retrieve_state(self, string header)
    cdef long assemble(self) except -1
    cdef long chunk(self) except -1

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
