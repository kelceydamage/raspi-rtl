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

from numpy cimport ndarray

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->

cdef class Squash:
    """
    NAME:           Squash

    DESCRIPTION:    A class of utility functions used by the datatypes.

    METHODS:        .countOutliers()
                    Sets the array values for the outliers exceeding the mean 
                    times two, to be equal to the mean times two.

                    .normalize()
                    Executes the normalization algorithm
    """
    cdef:
        public ndarray column
        float weight
        float max
        uint_fast8_t count
        float avg
        str _id

    cdef void countOutliers(self)
    cdef void normalize(self)

cdef class PercentOfMax:
    """
    NAME:           PercentOfMax

    DESCRIPTION:    A class of utility functions used by the datatypes.

    METHODS:        .normalize()
                    Executes the normalization algorithm
    """
    cdef:
        public ndarray column
        float weight
        float max
        uint_fast8_t count
        str _id

    cdef void normalize(self)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
