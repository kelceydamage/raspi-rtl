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
import ast
from rtl.common.task import Task
from numpy import ndarray
from numpy import array
import datetime

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class ConvertToNumeric(Task):

    def __init__(self, kwargs, content):
        super(ConvertToNumeric, self).__init__(kwargs, content)
        self.dtypes = self.schemaToDtype()
        self.appCount = 0
        self.jobCount = 0
        self.stageCount = 0
        self.rid = 0
        self.key = 0
        self.applications = {}
        self.jobs = {}
        self.stages ={}
        self.outputKeys = {}
        self.outputRids = {}

    def getAppID(self, app):
        if app in self.applications.keys():
            return self.applications[app]
        else:
            self.applications[app] = self.appCount
            self.appCount += 1
            return self.applications[app]

    def getJobID(self, job):
        if job in self.jobs.keys():
            return self.jobs[job]
        else:
            self.jobs[job] = self.jobCount
            self.jobCount += 1
            return self.jobs[job]

    def getStageID(self, stage):
        if stage in self.stages.keys():
            return self.stages[stage]
        else:
            self.stages[stage] = self.stageCount
            self.stageCount += 1
            return self.stages[stage]

    def getTimestamp(self, datestring):
        d = datetime.datetime.strptime(
            datestring, 
            '%Y-%m-%dT%H:%M:%S.%fZ'
            )
        return d.timestamp()

    def getMinFromHours(self, hours):
        return hours * 60

    def getMinFromSeconds(self, seconds):
        return seconds / 60

    def setColumns(self):
        self.dtypes = self.newColumns

    def initArray(self):
        #self.setColumns()
        self.ndata = np.zeros(
            (len(self.data), 1),
            dtype=np.dtype(self.dtypes)
        )

    def createOutputKey(self, keys):
        try:
            keys = keys.strip('[').strip(']').split(',')
            for k in keys:
                if k not in self.outputRids.keys():
                    self.outputRids[k] = self.rid 
                    self.rid += 1
            key = '-'.join([str(self.outputRids[j]) for j in keys])
            if key not in self.outputKeys.keys():
                self.outputKeys[key] = self.key
                self.key += 1
            return self.outputKeys[key]
        except Exception as e:
            print('ERROR4', e)

    def isSucessful(self, value):
        if value == 'SUCCEEDED':
            return True
        return False

    def schemaToDtype(self):
        try:
            return [tuple(x) for x in self.schema]
        except Exception as e:
            print('ERROR3', e)

    def parseSchema(self, n, v):
        try:
            if n == 0:
                return self.getJobID(v[n])
            elif n == 3:
                return self.getAppID(v[n])
            elif n == 4:
                return self.createOutputKey(v[n])
            elif n == 8:
                return self.isSucessful(v[n])
            elif n == 7:
                return self.getStageID(v[n])
            else:
                return v[n]
        except Exception as e:
            print('ERROR2', e)

    def convertToNumeric(self):
        self.initArray()
        for k, v in self.data.items():
            if 'appName' in v: continue
            try:
                self.ndata[k] = tuple([
                    self.parseSchema(n, v) 
                    for n in range(len(self.schema))
                ])
            except Exception as e:
                print('ERROR' + 'k', e)
        print(self.applications)
        return self


# Functions
# ------------------------------------------------------------------------ 79->
def task_custom_convert_to_numeric(kwargs, contents):
    return ConvertToNumeric(kwargs, contents).convertToNumeric().getContents()