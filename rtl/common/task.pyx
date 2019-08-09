#!python
#cython: language_level=3, cdivision=True
###boundscheck=False, wraparound=False //(Disabled by default)
# ------------------------------------------------------------------------ 79->
# Author: ${name=Kelcey Damage}
# Python: 3.5+
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
# Required Args:        
#
# Optional Args:        
#
# Imports
# ------------------------------------------------------------------------ 79->
import numpy as np
from rtl.transport.conf.configuration import DEBUG

cimport numpy as np
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
from numpy cimport dtype

# Globals
# ------------------------------------------------------------------------ 79->
ENCODING = 'utf-8'

# Classes
# ------------------------------------------------------------------------ 79->
cdef class Task:

    def __init__(Task self, dict kwargs, ndarray contents):
        super(Task, self).__init__()
        cdef:
            list keys = list(kwargs)
            int l = len(keys)
            int i

        self.ndata = contents
        self.dtypes = self.ndata.dtype
        for i in range(l):
            if isinstance(kwargs[keys[i]], str):
                kwargs[keys[i]] = kwargs[keys[i]].encode(ENCODING)
            setattr(self, keys[i], kwargs[keys[i]])

    cpdef ndarray getContents(Task self):
        if DEBUG: print('TASK: getContents')
        return self.ndata

    cpdef void addColumns(Task self):
        if DEBUG: print('TASK: addColumns')
        cdef:
            ndarray newrecarray
            int length = self.ndata.shape[0]
            tuple names = self.ndata.dtype.names
            int l = len(names)
            int i
            
        self.dtypes = dtype(self.dtypes.descr + self.newColumns)
        newrecarray = np.zeros(length, dtype=self.dtypes)
        for i in range(l):
            newrecarray[names[i]] = self.ndata[names[i]]
        self.ndata = newrecarray

    cpdef void setColumn(Task self, int i, ndarray v):
        if DEBUG: print('TASK: setColumn')
        self.ndata[self.newColumns[i][0]] = v

    cpdef void getLSpace(Task self, string space, ndarray x):
        if DEBUG: print('TASK: getLSpace')
        if x is None:
            raise TypeError
        if space == <string>b'log':
            self.lSpace = np.logspace(0.001, 1, x.shape[0], endpoint=True).reshape(-1, 1)
        elif space == <string>b'linear':
            self.lSpace = np.linspace(0, max(x), x.shape[0]).reshape(-1, 1)
        else:
            self.lSpace = np.sort(x, axis=0).reshape(-1, 1)