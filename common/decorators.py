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
from common.print_helpers import printc, Colours
import time

# ------------------------------------------------------------------------ 79->
COLOURS = Colours()

# Classes
# ------------------------------------------------------------------------ 79->
  
# Functions
# ------------------------------------------------------------------------ 79->
def timer(f):
    def _timer(self):
        start_time = time.perf_counter()
        r = f(self)
        end_time = time.perf_counter()
        printc('JOB COMPLETED: {0}s'.format(end_time - start_time), COLOURS.GREEN)
        return r
    return _timer


# Main
# ------------------------------------------------------------------------ 79->