#!/usr/bin/env python3
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
# Required Args:        'file'
#                       Name of the file to be opened.
#
#                       'path'
#                       Path to the file to be opened.
#
# Optional Args:        'delimiter'
#                       Value to split the file on. Default is '\n'.
#
#                       'compression'
#                       Boolean to denote zlib compression on file. Default is
#                       False.
#
# Imports
# ------------------------------------------------------------------------ 79->
import numpy as np

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class Task():

    def __init__(self, kwargs, contents):
        for item in kwargs.keys():
            setattr(self, item, kwargs[item])
        for item in contents.keys():
            setattr(self, item, contents[item])

    def getContents(self):
        return {
            'ndata': self.ndata,
            'data': self.data,
            'reduces': self.reduces,
            'dtypes': self.dtypes
        }

    def addColumns(self, newColumns):
        self.dtypes = self.dtypes + newColumns
        newrecarray = np.zeros(len(self.ndata), dtype = self.dtypes)
        for name in self.ndata.dtype.names:
            newrecarray[name] = self.ndata[name]
        self.ndata = newrecarray

    def getLSpace(self, space, x=None):
        if space == 'log':
            self.lSpace = np.logspace(0.001, 1, x.shape[0], endpoint=True).reshape(-1, 1)
        elif space == 'linear':
            self.lSpace = np.linspace(0, max(x), x.shape[0]).reshape(-1, 1)
        else:
            self.lSpace = np.sort(x, axis=0).reshape(-1, 1)