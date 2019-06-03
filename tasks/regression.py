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

# Imports
# ------------------------------------------------------------------------ 79->
import numpy as np
from common.task import Task
from common.regression import Models
#from common.print_helpers import lprint

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class LinearRegression(Task):

    def __init__(self, kwargs, contents):
        super(LinearRegression, self).__init__(kwargs, contents)
        self.newColumns = [
            ('{0}{1}'.format(o['y'], o['model']), '<f8') 
            for o in self.operations
        ]
        self.addColumns()

    def lookupModel(self, modelName):
        return Models.__dict__[modelName]

    def regress(self):
        for i in range(len(self.operations)):
            o = self.operations[i]
            args = None
            if o['model'] == 'Poly':
                args = o['d']
            self.getLSpace(o['space'], self.ndata[o['x']])
            M = self.lookupModel(o['model'])(
                self.ndata[o['x']],
                self.ndata[o['y']],
                self.lSpace,
                args
            )
            self.setColumn(
                i,
                M.prediction
            )
            # temp code
            print('=> Regression[{0}] Results: m={1}, c={2}, r={3}'.format(
                o['model'],
                M.m,
                M.c,
                M.r
            ))
        return self


# Functions
# ----------------------------------------------------------------------- 79->
def task_regression(kwargs, contents):
    Task = LinearRegression(
        kwargs['task_regression'],
        contents
    )
    return Task.regress().getContents()


# Main
# ------------------------------------------------------------------------ 79->
