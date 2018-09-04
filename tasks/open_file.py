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
from common.print_helpers import Logger
from transport.conf.configuration import LOG_LEVEL
import zlib
import ast
import ujson as json

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->


def configure(kwargs):
    keys = ['compression', 'delimiter', 'encoding']
    defaults = {'compression': False, 'delimiter': '\\n', 'encoding': False}
    params = []
    for key in keys:
        if key in kwargs['kwargs']:
            params.append(kwargs['kwargs'][key])
        else:
            params.append(defaults[key])
    return params


def _open(compression, file_path, file_name):
    mode = 'r'
    if compression:
        mode = 'rb'
    with open('{0}/{1}'.format(file_path, file_name), mode) as f:
        r = f.read()
        if compression:
            r = zlib.decompress(r).decode()
    return r


def decode(parts):
    results = []
    for i in range(len(parts)):
        item = parts.pop().strip('\n')
        if item != '':
            if encoding:
                item = json.loads(item.rstrip())
        results.append(item)
    return results


def task_open_file(kwargs):
    name = 'NODE-{0}'.format(kwargs['worker'])
    LOG.logc(name, 'starting task', 'open_file', 1, 'LIGHTBLUE')
    if kwargs['data'] != []:
        if kwargs['data'] == [False]:
            return [False]
    compression, delimiter, encoding = configure(kwargs)
    file_name = kwargs['kwargs']['file']
    file_path = kwargs['kwargs']['path']
    mode = 'r'
    r = _open(compression, file_path, file_name)
    parts = r.replace('][', ']\n[').split(delimiter)
    if parts == ['']:
        return [False]
    results = decode(parts)
    del parts
    return results

# Main
# ------------------------------------------------------------------------ 79->
