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
from common.task import Task
from common.normalization import Models

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class Normalize(Task):
    
    def __init__(self, kwargs, content):
        super(Normalize, self).__init__(kwargs, content)
        self.newColumns = [
            ('{0}Normal'.format(x), '<f8') 
            for x in self.columns
        ]
        self.addColumns()

    def lookupModel(self, modelName):
        if self.model is None: modelName = 'Null'
        return Models.__dict__[modelName]

    def normalize(self):
        for i in range(len(self.columns)):
            M = self.lookupModel(self.model)(
                self.ndata[self.columns[i]].tolist(),
                self.weight
            )
            self.setColumn(
                i,
                M.column
            )
        return self


# Functions
# ------------------------------------------------------------------------ 79->
def task_normalize(kwargs, contents):
    Task = Normalize(
        kwargs['task_normalize'], 
        contents
    )
    return Task.normalize().getContents()