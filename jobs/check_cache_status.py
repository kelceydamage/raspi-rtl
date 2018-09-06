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
from transport.conf.configuration import CACHE_PATH

# Globals
# ------------------------------------------------------------------------ 79->
HEADER = Tools.create_id()  # pragma: no cover
CACHE = Cache()  # pragma: no cover

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def test_cache_status():  # pragma: no cover
    print('TEST: (status)')
    r = CACHE.send('status')[1]
    print(r)


def test_cache_info():  # pragma: no cover
    print('TEST: (info)')
    r = CACHE.send('info')[1]
    print(r)


def test_cache_stale():  # pragma: no cover
    print('TEST: (stale)')
    r = CACHE.send('stale_readers')[1]
    print(r)


def test_cache_readers():  # pragma: no cover
    print('TEST: (path)')
    r = CACHE.send('path')[1]
    print(r)


def test_cache_locks():  # pragma: no cover
    print('TEST: (locks)')
    r = CACHE.send('locks')[1]
    print(r)


# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':  # pragma: no cover
    test_cache_status()
    test_cache_info()
    test_cache_stale()
    test_cache_readers()
    test_cache_locks()
