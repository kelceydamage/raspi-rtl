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

import numpy as np
import ast
from base64 import b64decode
import re
from common.task import Task

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class OpenArray(Task):

    def __init__(self, kwargs, content):
        super(OpenArray, self).__init__(kwargs, content)
        self.file = "{0}/{1}".format(self.path, self.filename)

    def decodeMeta(self, m):
        s = b64decode(m).decode('utf-8')
        d1 = re.compile('<@')
        d2 = re.compile('@>')
        s = d1.sub('(', s)
        s = d2.sub(')', s)
        self.dtypes = ast.literal_eval(s)

    def openMeta(self):
        with open('{0}.meta'.format(self.file), 'rb') as f:
            self.decodeMeta(f.read())

    def openArray(self):
        self.openMeta()
        self.ndata = np.loadtxt(
            "{0}/{1}.{2}".format(self.path, self.filename, self.extension), 
            delimiter=self.delimiter,
            dtype=self.dtypes
            )
        return self


# Functions
# ------------------------------------------------------------------------ 79->
def task_open_array(kwargs, contents):
    print(kwargs)
    Task = OpenArray(
        kwargs['task_open_array'],
        contents
    )
    return Task.openArray().getContents()

# Main
# ------------------------------------------------------------------------ 79->
