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
from common.task import Task

# Globals
# ------------------------------------------------------------------------ 79->
'''
(array([23, 29,  9,  7,  1,  0, 15,  0,  0,  0,  0,  0,  1,  0,  0,  0,  3,
       11,  0,  1]), array([  61.  ,  163.85,  266.7 ,  369.55,  472.4 ,  575.25,  678.1 ,
        780.95,  883.8 ,  986.65, 1089.5 , 1192.35, 1295.2 , 1398.05,
       1500.9 , 1603.75, 1706.6 , 1809.45, 1912.3 , 2015.15, 2118.  ]))
'''

# Classes
# ------------------------------------------------------------------------ 79->
class Histogram(Task):

    def __init__(self, kwargs, content):
        super(Histogram, self).__init__(kwargs, content)
        self.newColumns = [
            ('{0}'.format(o['column']), '<f8')
            for o in self.operations
        ]
        self.addColumns()

    def getBucket(self, value):
        for i in range(len(self.buckets)):
            if self.buckets[i] >= value:
                return self.buckets[i]

    def tagRows(self, array):
        values = []
        for i in range(len(array)):
            values.append(self.getBucket(array[i]))
        return values

    def histogram(self):
        for i in range(len(self.operations)):
            o = self.operations[i]
            avg = np.mean(self.ndata[o['a']])
            histogram = np.histogram(
                    self.ndata[o['a']], 
                    o['bins']
                )
            self.buckets = histogram[1]
            self.setColumn(
                i,
                self.tagRows(self.ndata[o['a']])
            )
        return self


# Functions
# ------------------------------------------------------------------------ 79->
def task_histogram(kwargs, contents):
    return Histogram(kwargs, contents).histogram().getContents()

# Main
# ------------------------------------------------------------------------ 79->
