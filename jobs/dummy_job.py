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
            #os.path.dirname(
                os.path.abspath(__file__)
                )
            #)
        )
    )
import zmq
from transport.dispatch import Dispatcher
from common.datatypes import *
from common.print_helpers import *

# Globals
# ------------------------------------------------------------------------ 79->
COLOURS = Colours()
COUNT = 2

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    dispatcher = Dispatcher()
    meta = Meta()
    pipeline = Pipeline()
    data = [[1, 2, 3], [2, 3 ,4], [5, 3 ,4], [1, 2, 3]]
    envelope = Envelope()
    header = Tools.create_id()
    pipeline.tasks = ['task_sum', 'task_sum', 'task_sum', 'task_sum']
    meta.lifespan = 3
    
    envelope.pack(header, meta.extract(), pipeline.extract(), data)
    envelope = dispatcher.send(envelope)

    print(envelope.open())
    printc('JOB COMPLETED', COLOURS.GREEN)