#!/usr/bin/env python
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
"""
Dependancies:
    rtl.transport
    rtl.common

"""
# Imports
# ------------------------------------------------------------------------ 79->
from rtl.transport.conf.configuration import DEBUG
from rtl.common.print_helpers import Colours
from rtl.common.print_helpers import printc


# Functions
# ------------------------------------------------------------------------ 79->
def log(msg):
    """If debug (bool) is true, then print the message"""
    if DEBUG:
        printc(msg, Colours().RED)
