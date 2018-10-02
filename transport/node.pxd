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

# Python imports
from common.datatypes cimport Envelope

# Cython imports
cimport cython
from libcpp.string cimport string
from libc.stdint cimport uint_fast16_t

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
        string version
        string header
        string domain_id

    cdef void recv(self)
    cdef void send(self)
    cpdef void start(self)


cdef class TaskNode(Node):
    cdef:
        public object recv_socket
        public object send_socket
        public dict functions

    cpdef void run(self)


cdef class CacheNode(Node):
    cdef:
        public object recv_socket
        public object lmdb

    cpdef void load_database(self)


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
