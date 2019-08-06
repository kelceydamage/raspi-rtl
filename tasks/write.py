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
from base64 import b64encode, b64decode
import re
import ujson as json
from common.task import Task

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class Write(Task):

    def __init__(self, kwargs, content):
        super(Write, self).__init__(kwargs, content)
        self.file = "{0}/{1}".format(self.path.decode('utf-8'), self.filename.decode('utf-8'))

    def formatColumns(self):
        types = [x[1] for x in self.dtypes]
        fmt = []
        for x in types:
            if x == '<i8':
                fmt.append('%i')
            elif x == '<f8':
                fmt.append('%f')
            else:
                print('ERR', x)
        return ','.join(fmt)

    def encodeMeta(self):
        s = str(self.dtypes)
        p1 = re.compile('\)')
        p2 = re.compile('\(')
        s = p1.sub('@>', s)
        s = p2.sub('<@', s)
        b = b64encode(s.encode('utf-8'))
        return b64encode(s.encode('utf-8'))

    def writeMeta(self):
        with open('{0}.meta'.format(self.file), 'wb') as f:
            f.write(self.encodeMeta())

    def write(self):
        print(self.extension)
        if self.extension == b'csv':
            self.writeCSV()
        elif self.extension == b'dat':
            self.writeNPBinary()
        return self

    def writeNPBinary(self):
        fmt = self.formatColumns()
        with open("{0}.{1}".format(self.file, self.extension.decode('utf-8')), 'wb') as f:
            f.write(self.ndata.tobytes())
        self.writeMeta()

    def writeCSV(self):
        fmt = self.formatColumns()
        np.savetxt(
            "{0}.{1}".format(self.file, self.extension), 
            self.ndata,
            delimiter=self.delimiter,
            fmt=fmt
            )
        self.writeMeta()


# Functions
# ------------------------------------------------------------------------ 79->
def task_write(kwargs, contents):
    Task = Write(
        kwargs['task_write'],
        contents
    )
    return Task.write().getContents()

# Main
# ------------------------------------------------------------------------ 79->
