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
#
# Imports
# ------------------------------------------------------------------------ 79->

import numpy as np
import ast
from base64 import b64decode
import re
from common.task import Task
import csv
import mmap
import time

cimport numpy as np
from libcpp.string cimport string
from libc.stdio cimport fopen, FILE, fclose
from posix.stdio cimport fileno
from common.task cimport Task
from numpy cimport ndarray

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
cdef class OpenArray(Task):
    cdef:
        public string file
        public string path
        public string filename
        public string delimiter
        public string extension

    def __init__(OpenArray self, dict kwargs, dict content):
        super(OpenArray, self).__init__(kwargs, content)
        self.file = self.path.append(b'/').append(self.filename)

    cdef void decodeMeta(OpenArray self, string m):
        cdef:
            string s
            object d1
            object d2
            double t
        
        s = b64decode(m)
        d1 = re.compile(b'<@')
        d2 = re.compile(b'@>')
        s = d1.sub(b'(', s)
        s = d2.sub(b')', s)

        self.dtypes = ast.literal_eval(s.decode('utf-8'))

    cdef void openMeta(OpenArray self):
        cdef:
            string filemeta
        
        with open(filemeta.append(self.file).append(b'.meta'), 'rb') as f:
            self.decodeMeta(f.read())

    cdef void openCSV(OpenArray self):
        cdef:
            string filedata
            list _b = []

        with open(filedata.append(self.file).append(b'.').append(self.extension), 'rb') as f:
            _b = [tuple(line.split(self.delimiter)) for line in f]
            self.ndata = np.asarray(_b, dtype=self.dtypes)

    cdef void openNPBinary(OpenArray self):
        cdef:
            string filedata

        self.ndata = np.memmap(
            filedata.append(self.file).append(b'.').append(self.extension), 
            mode='r',
            dtype=self.dtypes
        )

    cdef OpenArray openArray(OpenArray self):
        self.openMeta()
        if self.extension == b'csv':
            self.openCSV()
        elif self.extension == b'dat':
            self.openNPBinary()
        return self


# Functions
# ------------------------------------------------------------------------ 79->
cpdef dict task_open_array(dict kwargs, dict contents):
    cdef:
        OpenArray Task

    Task = OpenArray(
        kwargs['task_open_array'],
        contents
    )
    return Task.openArray().getContents()

# Main
# ------------------------------------------------------------------------ 79->
