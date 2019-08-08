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
from web.plot import PLOT_QUEUE


# Globals
# ------------------------------------------------------------------------ 79->


# Classes
# ------------------------------------------------------------------------ 79->
class Plot(Task):

    def __init__(self, kwargs, contents):
        super(Plot, self).__init__(kwargs, contents)
        self.queue = PLOT_QUEUE

    def getSeries(self, series):
        if series is None:
            return None
        return self.ndata[series].tolist()

    def plot(self):
        for plot in self.plots.keys():
            draws = []
            for draw in self.plots[plot]:
                draws.append(
                    {
                        'type': draw['type'], 
                        'x': self.ndata[draw['x']].tolist(), 
                        'y': self.ndata[draw['y']].tolist(),
                        'series': self.getSeries(draw['series'])
                    }
                )
            self.queue.put({
                'name': plot,
                'draws': draws,
                'xAxis': self.plots[plot][0]['x'],
                'yAxis': self.plots[plot][0]['y'],
                'scale': self.plots[plot][0]['scale']
            })
        return self


# Functions
# ------------------------------------------------------------------------ 79->
def task_simple_plot(kwargs, contents):
    return Plot(kwargs, contents).plot().getContents()

# Main
# ------------------------------------------------------------------------ 79->
