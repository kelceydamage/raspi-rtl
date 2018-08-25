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

# Imports
# ------------------------------------------------------------------------ 79->
from common.print_helpers import Logger
from transport.conf.configuration import LOG_LEVEL
import zlib
import time

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def configure(kwargs):
    delimiter = '\n'
    compression = False
    if 'compression' in kwargs['kwargs']:
        compression = kwargs['kwargs']['compression']
    if 'delimiter' in kwargs['kwargs']:
        delimiter = kwargs['kwargs']['delimiter']
    return compression, delimiter

def task_open_file(kwargs):
    compression, delimiter = configure(kwargs)
    name = 'NODE-{0}'.format(kwargs['worker'])
    LOG.logc(name, 'starting task', 'open_file', 1, 'LIGHTBLUE')
    file_name = kwargs['kwargs']['file']
    file_path = kwargs['kwargs']['path']
    with open('{0}/{1}'.format(file_path, file_name), 'rb') as f:
        r = f.read()
        if compression:
            r = zlib.decompress(r).decode()
    parts = r.split(delimiter)
    results = []
    for i in range(len(parts)):
        results.append(parts.pop().strip('\n'))
    del parts
    return results

# Main
# ------------------------------------------------------------------------ 79->
