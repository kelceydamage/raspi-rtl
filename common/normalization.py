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

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class Null():

    def __init__(self, column, weight):
        self.column = column

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


class Models():
    DistanceFromMean = DistanceFromMean
    Null = Null


# Functions
# ------------------------------------------------------------------------ 79->
