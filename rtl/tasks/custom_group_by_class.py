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
from rtl.common.task import Task

# Globals
# ------------------------------------------------------------------------ 79->
# filter
# aggregate
# 

# Classes
# ------------------------------------------------------------------------ 79->
class GroupByClass(Task):

    def __init__(self, kwargs, content):
        super(GroupByClass, self).__init__(kwargs, content)
        self.newColumns = [
            ('{0}GB{1}'.format(o['target'], o['func']), '<i8')
            for o in self.operations
        ]
        self.addColumns()

    def createGrouping(self, _class, target, func):
        grouped = {}
        for i in range(len(self.ndata)):
            if self.ndata[i][_class] in grouped.keys():
                grouped[self.ndata[i][_class]] = func(
                    [
                        self.ndata[i][target],
                        grouped[self.ndata[i][_class]]
                    ]
                )
            else:
                grouped[self.ndata[i][_class]] = self.ndata[i][target]
        return grouped

    def applyGrouping(self, grouped, _class):
        values = []
        for r in self.ndata:
            values.append(grouped[r[_class]])
        return values

    def groupByClass(self):
        for i in range(len(self.operations)):
            o = self.operations[i]
            if o['func'] == 'min':
                func = min
            elif o['func'] == 'sum':
                func = sum
            else:
                func = max
            grouped = self.createGrouping(
                o['class'], 
                o['target'],
                func
             )
            values = self.applyGrouping(grouped, o['class'])
            self.setColumn(
                i,
                values
            )
        return self
    

# Functions
# ------------------------------------------------------------------------ 79->
def task_custom_group_by_class(kwargs, contents):
    return GroupByClass(kwargs, contents).groupByClass().getContents()