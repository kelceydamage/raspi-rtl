#!python
#cython: language_level=3, cdivision=True
###boundscheck=False, wraparound=False //(Disabled by default)
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

    def __init__(self, x, y, lSpace=None, args=None):
        self.x = x.reshape(-1, 1)
        self.y = y
        self.lSpace = lSpace
        self.regress()

    def regress(self):
        self.model = LinearRegression().fit(self.x, self.y)
        self.m = self.model.coef_[0]
        self.c = self.model.intercept_
        self.r = self.model.score(self.x, self.y)
        if self.lSpace is None:
            self.lSpace = np.sort(self.x, axis=0)
        self.prediction = self.model.predict(self.lSpace)

class Poly():

    def __init__(self, x, y, lSpace=None, args=None):
        self.x = x
        self.y = y
        self.lSpace = lSpace
        self.d = args
        self.regress()

    def regress(self):
        self.m = np.polyfit(self.x, self.y, self.d)
        self.c = None
        self.r = None
        f = np.poly1d(self.m)
        if self.lSpace is None:
            self.lSpace = np.sort(self.x, axis=0)
        self.prediction = f(self.lSpace).reshape(-1)


class Models():
    Linear = Linear
    Poly = Poly


# Functions
# ------------------------------------------------------------------------ 79->
