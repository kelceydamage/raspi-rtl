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
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from rtl.common.transform import Transform

# Globals
# ------------------------------------------------------------------------ 79->
FILENAME = 'output27Numeric'

# Classes
# ------------------------------------------------------------------------ 79->
DSDSL = {
    0: {
        'tasks': {
            'task_open_array': {
                'filename': FILENAME,
                'path': 'raw_data',
                'extension': 'dat',
                'delimiter': ','
            }
        }
    },
    1: {
        'tasks': {
            'task_filter': {
                'operations': [
                    {
                        'column': 'appName',
                        'value': 0,
                        'method': 'eq'
                    },
                    {
                        'column': 'stageName',
                        'value': 22,
                        'method': 'eq'
                    },
                    {
                        'column': 'jobId',
                        'value': 1500,
                        'method': 'gt'
                    },
                    {
                        'column': 'totalRunTime',
                        'value': 1000,
                        'method': 'lt'
                    }
                ]
            },
            'task_add': {
                'operations': [
                    {
                        'a': 'inputBytesRead',
                        'b': 'shuffleLocalBytesRead',
                        'column': 'a1'
                    },
                    {
                        'a': 'a1',
                        'b': 'shuffleRemoteBytesRead',
                        'column': 'totalReadBytes'
                    }
                ]
            },
            'task_divide': {
                'operations': [
                    {
                        'a': 'totalRunTime',
                        'b': 'numTasks',
                        'column': 'concurrentRunTime'
                    },
                    {
                        'a': 'totalReadBytes',
                        'b': 'numTasks',
                        'column': 'concurrentReadBytes'
                    },
                ]
            },
            'task_normalize': {
                'model': 'Squash',
                'columns': [
                    'totalRunTime',
                    'totalReadBytes',
                    'concurrentRunTime',
                    'concurrentReadBytes'
                ],
                'weight': None
            },
            'task_subtract': {
                'operations': [
                    {
                        'a': 'totalRunTimeNormal',
                        'b': 'totalReadBytesNormal',
                        'column': 'difference1'
                    },
                    {
                        'a': 'concurrentRunTimeNormal',
                        'b': 'concurrentReadBytesNormal',
                        'column': 'difference2'
                    }
                ]
            },
            'task_average': {
                'operations': [
                    {
                        'a': 'difference1',
                        'column': 'alphaAvg1'
                    },
                    {
                        'a': 'difference2',
                        'column': 'alphaAvg2'
                    }
                ]
            },
            'task_simple_plot': {
                'plots': {
                    'concurrentRunTime': [
                        {
                            'y': 'concurrentRunTimeNormal',
                            'x': 'jobId',
                            'type': 'circle',
                            'scale': 'linear',
                            'series': 'outputDatasetRids'
                        },
                    ],
                    'concurrentReadBytes': [
                        {
                            'y': 'concurrentReadBytesNormal',
                            'x': 'jobId',
                            'type': 'circle',
                            'scale': 'linear',
                            'series': 'outputDatasetRids'
                        },
                    ],
                    'totalRuntime - totalBytesRead': [
                        {
                            'y': 'difference1',
                            'x': 'jobId',
                            'type': 'circle',
                            'scale': 'linear',
                            'series': 'outputDatasetRids'
                        },
                    ],
                    'totalRuntime(conc) - totalBytesRead(conc)': [
                        {
                            'y': 'difference2',
                            'x': 'jobId',
                            'type': 'circle',
                            'scale': 'linear',
                            'series': 'outputDatasetRids'
                        },
                    ],
                    'totalRuntime(conc) - totalBytesRead(conc) 2': [
                        {
                            'y': 'difference2',
                            'x': 'jobId',
                            'type': 'circle',
                            'scale': 'linear',
                            'series': 'outputDatasetRids'
                        },
                    ],
                }
            }
        }
    }
}


# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    print(Transform().execute(DSDSL).result())
