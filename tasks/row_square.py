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
from numpy import ndarray
from numpy import array
import datetime

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class Utils():

    def __init__(self, kwargs):
        pass

    def validate(self, ndata):
        if ndata != [[]]:
            if ndata[0].any() == [False]:
                return False
            return True
        return True

# Functions
# ------------------------------------------------------------------------ 79->
def task_row_square(kwargs, ndata, data):
    U = Utils(kwargs)
    if not U.validate(ndata): return [[False]]
    ndata.setflags(write=1)
    for i in range(ndata.shape[0]):
        ndata[i] = np.multiply(ndata[i], ndata[i])
    return ndata, data


# Main
# ------------------------------------------------------------------------ 79->
