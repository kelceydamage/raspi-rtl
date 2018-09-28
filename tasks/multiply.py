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
import numpy as np
from common.print_helpers import Logger
from common.print_helpers import timer
from transport.conf.configuration import PROFILE
from transport.conf.configuration import LOG_LEVEL

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->


@timer(LOG, 'task_multiply', PROFILE)
def task_multiply(kwargs, data):
    data.setflags(write=1)
    for i in range(data.shape[0]):
        data[i] = np.multiply(data[i], data[i])
    return data


# Main
# ------------------------------------------------------------------------ 79->