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
from transport.dispatch import Cache
from common.datatypes import Tools

# Globals
# ------------------------------------------------------------------------ 79->
HEADER = Tools.create_id() # pragma: no cover
CACHE = Cache() # pragma: no cover

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def test_cache_check(): # pragma: no cover
    print(HEADER)
    r = CACHE.send('check', HEADER)
    print(r)
    assert r[1] == False

def test_cache_set(): # pragma: no cover
    r = CACHE.send('set', HEADER, 'test data')
    assert r[1] == True

def test_cache_get(): # pragma: no cover
    r = CACHE.send('get', HEADER, 'test data')
    assert r[1] == 'test data'

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__': # pragma: no cover
    test_cache_check()
    test_cache_set()
    test_cache_get()