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
from transport.dispatch import Dispatcher
from common import datatypes
from common.print_helpers import printc, Colours, print_stage
from common.decorators import timer
import time
import numpy as np
import cbor
import io

# ------------------------------------------------------------------------ 79->
COLOURS = Colours()

# Classes
# ------------------------------------------------------------------------ 79->
class Transform:

    def __init__(self):
        self.dispatcher = Dispatcher()
        self.envelope = datatypes.Envelope(cached=False)

    @timer
    def run(self):
        self.envelope = self.dispatcher.send(self.envelope)
        print(self.envelope.header)

    def validateSchema(self, schema):
        r = [x for x in ['tasks', 'kwargs', 'data', 'ndata'] if x not in schema.keys()]
        if len(r) > 0:
            printc('FAIL: missing key: {0} in schema'.format(r), COLOURS.RED)
            exit(1)
        if schema['tasks'] is None or not isinstance(schema['tasks'], list):
            printc('FAIL: missing/malformed task list in schema'.format(r), COLOURS.RED)
            exit(0)

    def execute(self):
        stages = [x for x in dir(self) if 'stage' in x]
        stages.sort()
        for stage in stages:
            method = getattr(self, stage)
            schema = method()
            self.validateSchema(schema)
            self.envelope.pack(
                meta={
                    'tasks': schema['tasks'],
                    'completed': [], 
                    'kwargs': schema['kwargs']
                    }, 
                ndata=schema['ndata'],
                data=schema['data']
                )
            print_stage(stage, schema['tasks'])
            self.run()
        return self.envelope


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->