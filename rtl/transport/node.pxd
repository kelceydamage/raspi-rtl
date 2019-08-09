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
#                   libcpp.string
#                   libcpp.uint_fast16_t
#
# Imports
# ------------------------------------------------------------------------ 79->

# Cython imports
cimport cython
from libcpp.string cimport string
from libcpp.vector cimport vector
from libc.stdint cimport uint_fast16_t
from rtl.common.datatypes cimport Envelope

# Globals
# ------------------------------------------------------------------------ 79->

VERSION = '2.0a'

# Classes
# ------------------------------------------------------------------------ 79->


cdef class Node:
    cdef:
        uint_fast16_t pid
        Envelope envelope
        object _context
        object cache
        string version
        string header
        string domain_id
        object recv_poller

    # Python acccessible API
    cpdef void start(self)

    # CPP/Cython acccessible API
    cdef void recv(self)
    cdef void send(self)
    

cdef class TaskNode(Node):
    cdef:
        public object recv_socket
        public object send_socket
        public dict functions
        object jobQueue

    # Python acccessible API
    cpdef void run(self)

    # CPP/Cython acccessible API
    cdef void populateJobQueue(self, bytes id)


cdef class PlotNode(Node):
    cdef:
        public object server

    # Python acccessible API
    cpdef void start(self)


cdef class CacheNode(Node):
    cdef:
        public object recv_socket
        public object lmdb

    # Python acccessible API
    cpdef void load_database(self)


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
