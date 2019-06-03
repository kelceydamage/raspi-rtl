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

import zlib
import ast
import ujson as json
import numpy as np
from numpy import ndarray
from numpy import array
from common.task import Task

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class Open(Task):

    def __init__(self, kwargs, content):
        super(Open, self).__init__(kwargs, content)
        self.ndata.setflags(write=1)
        self.keys = [
            'compression', 
            'delimiter', 
            'encoding'
            ]
        self.defaults = {
            'compression': False, 
            'delimiter': '\n', 
            'encoding': False
            }
        self.configuration = {}
        self.mode = 'r'
        for key in self.keys:
            if key in kwargs:
                self.configuration[key] = kwargs[key]
            else:
                self.configuration[key] = self.defaults[key]

    def openfile(self):
        if self.configuration['compression']:
            self.mode = 'rb'
        with open('{0}/{1}'.format(self.path, self.file), self.mode) as f:
            r = f.read()
            if self.configuration['compression']:
                r = zlib.decompress(r).decode()
        parts = r.replace('][', ']\n[').split('\n')
        return parts

    def decode(self, parts):
        results = []
        while parts:
            item = parts.pop().strip('\n')
            if item == '':
                continue
            if self.configuration['encoding']:
                item = json.loads(item.rstrip())
            else:
                item = item.rstrip().split(self.configuration['delimiter'])
            results.append(item)
        return results

    def open(self):
        parts = self.openfile()
        if parts == [''] or parts == '':
            return [[False]]
        results = self.decode(parts)
        del parts
        if self.mixed:
            self.data = {i: results[i] for i in range(len(results))}
            self.data['headers'] = self.headers
        else:
            self.ndata = np.ndarray(
                (len(results), len(results[0])),
                buffer=array(results),
                dtype=np.dtype(int)
            )
        return self


# Functions
# ------------------------------------------------------------------------ 79->
def task_open(kwargs, contents):
    Task = Open(
        kwargs['task_open'],
        contents
    )
    return Task.open().getContents()

# Main
# ------------------------------------------------------------------------ 79->
