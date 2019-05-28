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

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class LinearRegression(Task):

    def __init__(self, kwargs, contents):
        super(LinearRegression, self).__init__(kwargs, contents)
        self.newColumns = [('regression', '<f8'), ('regressionX', '<i8')]

    def lookupModel(self, modelName):
        return Models.__dict__[modelName]

    def regress(self):
        self.addColumns(self.newColumns)
        M = self.lookupModel(self.model)(
            self.ndata[self.x],
            self.ndata[self.y],
            self.getLSpace(self.space)
        )
        self.ndata['regression'] = M.prediction
        self.ndata['regressionX'] = M.lSpace.reshape(1, -1)[0]
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
