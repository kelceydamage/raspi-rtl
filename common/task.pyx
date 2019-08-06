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

# Globals
# ------------------------------------------------------------------------ 79->
ENCODING = 'utf-8'

# Classes
# ------------------------------------------------------------------------ 79->
cdef class Task:

    def __init__(Task self, dict kwargs, dict contents):
        super(Task, self).__init__()
        cdef:
            list keys1 = list(kwargs)
            list keys2 = list(contents)
            int l1 = len(keys1)
            int l2 = len(keys2)
            int i

        for i in range(l1):
            if isinstance(kwargs[keys1[i]], str):
                kwargs[keys1[i]] = kwargs[keys1[i]].encode(ENCODING)
            setattr(
                self, 
                keys1[i],
                kwargs[keys1[i]]
            )
        for i in range(l2):
            if isinstance(contents[keys2[i]], str):
                contents[keys2[i]] = contents[keys2[i]].encode(ENCODING)
            setattr(
                self, 
                keys2[i],
                contents[keys2[i]]
            )

    cpdef dict getContents(Task self):
        return {
            'ndata': self.ndata,
            'data': self.data,
            'reduces': self.reduces,
            'dtypes': self.dtypes
        }

    cpdef void addColumns(Task self):
        cdef:
            ndarray newrecarray
            int l = len(self.ndata)
            tuple names = self.ndata.dtype.names
            int l2 = len(names)
            # int l3 = self.newColumns.size()
            int i

        # for i in range(l3):
        #     self.dtypes.push_back(self.newColumns[i])
        self.dtypes += self.newColumns
        newrecarray = np.zeros(l, dtype=self.dtypes)
        for i in range(l2):
            newrecarray[names[i]] = self.ndata[names[i]]
        self.ndata = newrecarray

    cpdef void setColumn(Task self, int i, ndarray v):
        # removed argument int r=-1
        #if r == -1:

        self.ndata[self.newColumns[i][0]] = v

        #else:
        #    self.ndata[r][self.newColumns[i][0]] = v

    cpdef void getLSpace(Task self, string space, ndarray x):
        if x is None:
            raise TypeError
        if space == <string>b'log':
            self.lSpace = np.logspace(0.001, 1, x.shape[0], endpoint=True).reshape(-1, 1)
        elif space == <string>b'linear':
            self.lSpace = np.linspace(0, max(x), x.shape[0]).reshape(-1, 1)
        else:
            self.lSpace = np.sort(x, axis=0).reshape(-1, 1)