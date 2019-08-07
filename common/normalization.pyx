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
from numpy cimport ndarray

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->

class DistanceFromMean():

    def __init__(self, column, weight):
        self.column = column
        self.weight = weight
        self.positiveRange = []
        self.negativeRange = []
        self.meanRange = []
        self.rangemod = 3
        self.count = len(self.column)
        self.normalize()

    def normalize(self):
        for i in range(self.count):
            localRange = self.getLocalRange(i)
            self.populateThresholds(localRange)
            self.updateValue(i)

    def getLocalRange(self, i):
        if i != 0 and i <= self.count - 2:
            return [
                self.column[i - 1],
                self.column[i],
                self.column[i + 1]
            ]
        return [self.column[i] for n in range(self.rangemod)]

    def populateThresholds(self, localRange):
        localMean = sum(localRange) / self.rangemod
        self.positiveRange.append(
            localMean + (localMean * self.weight)
        )
        self.negativeRange.append(
            localMean - (localMean * self.weight)
        )
        self.meanRange.append(localMean)

    def updateValue(self, i):
        if self.column[i] > self.positiveRange[i]:
            self.column[i] = self.positiveRange[i]
        elif self.column[i] < self.negativeRange[i]:
            self.column[i] = self.negativeRange[i]


cdef class PercentOfMax:

    def __init__(self, column, weight):
        self.column = column
        self.weight = min(self.column)
        self.max = max(self.column) - self.weight
        self.count = len(self.column)
        self.normalize()

    cdef void normalize(self):
        print('MAX', self.max, 'MIN', self.weight)
        for i in range(self.count):
            n = ((self.column[i] - self.weight) / self.max) * 100
            self.column[i] = n


cdef class Squash:

    def __init__(self, column, weight):
        self.column = column
        self.weight = min(self.column)
        self.max = max(self.column) - self.weight
        self.count = len(self.column)
        self.avg = sum(self.column) / self.count
        self.normalize()

    cdef void countOutliers(self):
        cdef:
            list temp = []

        for i in range(self.count):
            if self.column[i] > self.avg * 2:
                temp.append(self.column[i])
                self.column[i] = self.avg * 2
        self.max = max(self.column)

    cdef void normalize(self):
        self.countOutliers()
        print('MAX', self.max, 'MIN', self.weight, 'AVG', self.avg, 'COUNT', self.count)
        for i in range(self.count):
            n = ((self.column[i] - self.weight) / self.max) * 100
            self.column[i] = n


class Models():
    DistanceFromMean = DistanceFromMean
    PercentOfMax = PercentOfMax
    Squash = Squash


# Functions
# ------------------------------------------------------------------------ 79->
