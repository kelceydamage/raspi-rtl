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
from sklearn.linear_model import LinearRegression

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class Linear():

    def __init__(self, xValues, yValues, lSpace=None):
        self.xValues = xValues.reshape(-1, 1)
        self.yValues = yValues
        self.lSpace = lSpace
        self.regress()

    def regress(self):
        self.model = LinearRegression().fit(self.xValues, self.yValues)
        self.m = self.model.coef_[0]
        self.c = self.model.intercept_
        self.r = self.model.score(self.xValues, self.yValues)
        if self.lSpace is None:
            self.lSpace = self.xValues
        self.prediction = self.model.predict(self.lSpace)


class Models():
    Linear = Linear


# Functions
# ------------------------------------------------------------------------ 79->
