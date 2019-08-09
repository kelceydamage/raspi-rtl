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
#
# Imports
# ------------------------------------------------------------------------ 79->

import zlib
import ast
import ujson as json
import numpy as np
from numpy import ndarray
from numpy import array
from rtl.common.task import Task
import csv

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class Open(Task):

    def __init__(self, kwargs, content):
        super(Open, self).__init__(kwargs, content)
        self.mode = 'r'

    def openfile(self):
        with open('{0}/{1}'.format(self.path.decode('utf-8'), self.file.decode('utf-8')), self.mode) as f:
            table = csv.reader(f)
            c = 0
            for row in table:
                self.data[c] = row
                c += 1

    def open(self):
        #del self.data['d']
        self.openfile()
        return self


# Functions
# ------------------------------------------------------------------------ 79->
def task_custom_open(kwargs, contents):
    return Open(kwargs, contents).open().getContents()

# Main
# ------------------------------------------------------------------------ 79->
