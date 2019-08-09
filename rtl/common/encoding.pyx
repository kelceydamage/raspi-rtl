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
#

# Imports
# ------------------------------------------------------------------------ 79->
import hashlib
import uuid
import cbor
import zlib

cimport cython
from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.string cimport string
from libcpp.map cimport map
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast8_t
from libc.stdint cimport int_fast16_t
from libc.stdio cimport printf
from libc.stdlib cimport atoi
from posix cimport time as p_time

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->


cdef class Tools:
    """
    NAME:           Tools

    DESCRIPTION:    A class of utility functions used by the datatypes.

    METHODS:        .serialize(obj)
                    Converts an object into a bytes encoded serialized object.

                    .deserialize(obj)
                    Converts a bytes encoded serialized object back into an
                    object.

                    .create_header(meta)
                    Creates a bytes encoded hash(md5) of the metadata.

                    .create_id()
                    Creates a bytes encoded UUID4.
    """

    cpdef string serialize(self, object obj):
        return cbor.dumps(obj)

    cpdef object deserialize(self, bytes obj):
        return cbor.loads(obj)

    cpdef string create_header(self, object obj):
        return hashlib.md5(cbor.dumps(obj)).hexdigest().encode()

    cpdef string create_key(self, object obj):
        return hashlib.sha256(cbor.dumps(obj)).hexdigest()

    cdef string create_id(self):
        return <string>str(uuid.uuid4()).encode()


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
