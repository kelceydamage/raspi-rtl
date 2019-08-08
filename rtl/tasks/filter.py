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
class Filter(Task):

    def __init__(self, kwargs, content):
        super(Filter, self).__init__(kwargs, content)

    def filter(self):
        for o in self.operations:
            if o['method'] == 'eq':
                self.ndata = np.extract(
                    self.ndata[o['column']]==o['value'], 
                    self.ndata
                )
            elif o['method'] == 'ne':
                self.ndata = np.extract(
                    self.ndata[o['column']]!=o['value'], 
                    self.ndata
                )
            elif o['method'] == 'le':
                self.ndata = np.extract(
                    self.ndata[o['column']]>=o['value'], 
                    self.ndata
                )
            elif o['method'] == 'ge':
                self.ndata = np.extract(
                    self.ndata[o['column']]<=o['value'], 
                    self.ndata
                )
            elif o['method'] == 'lt':
                self.ndata = np.extract(
                    self.ndata[o['column']]>o['value'], 
                    self.ndata
                )
            elif o['method'] == 'gt':
                self.ndata = np.extract(
                    self.ndata[o['column']]<o['value'], 
                    self.ndata
                )
            print('=> Filtered Results: {0}'.format(self.ndata.shape))
        return self
    

# Functions
# ------------------------------------------------------------------------ 79->
def task_filter(kwargs, contents):
    return Filter(kwargs, contents).filter().getContents()

# Main
# ------------------------------------------------------------------------ 79->
