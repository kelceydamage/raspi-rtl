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

# Classes
# ------------------------------------------------------------------------ 79->
class ClassifyStatic(Task):

    def __init__(self, kwargs, content):
        super(ClassifyStatic, self).__init__(kwargs, content)
        self.newColumns = [
            ('{0}Class'.format(o['column']), '<i8')
            for o in self.operations
        ]
        self.newColumns += [
            ('{0}ClassCount'.format(o['column']), '<i8')
            for o in self.operations
        ]
        self.addColumns()

    def formKey(self, keys):
        if not isinstance(keys, list):
            keys = str(keys.astype(int))
            return keys
        return '-'.join([str(k) for k in keys])

    def createClasses(self, combinations, counts):
        classes = {}
        for i in range(len(combinations)):
            classes[self.formKey(combinations[i])] = (i, counts[i])
        return classes

    def applyClass(self, _classes, keys):
        classes = []
        counts = []
        for i in self.ndata:
            key = self.formKey(i[keys])
            classes.append(_classes[key][0])
            counts.append(_classes[key][1])
        return classes, counts

    def classifyStatic(self):
        for i in range(len(self.operations)):
            o = self.operations[i]
            unique, counts = np.unique(
                self.ndata[o['a']],
                return_counts=True,
                axis=0
                )
            _classes = self.createClasses(unique, counts)
            classes, counts = self.applyClass(_classes, o['a'])
            self.setColumn(
                i,
                classes
            )
            self.setColumn(
                i + len(self.operations),
                counts
            )
        return self
    

# Functions
# ------------------------------------------------------------------------ 79->
def task_classify_static(kwargs, contents):
    Task = ClassifyStatic(
        kwargs['task_classify_static'],
        contents
    )
    return Task.classifyStatic().getContents()

# Main
# ------------------------------------------------------------------------ 79->
