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


def test_cache_check():  # pragma: no cover
    print('TEST: (check)')
    assert str(CACHE.send('check', HEADER)[1]) == 'False'


def test_cache_set():  # pragma: no cover
    print('TEST: (set)')
    assert str(CACHE.send('set', HEADER, 'test data')[1]) == 'True'


def test_cache_get():  # pragma: no cover
    print('TEST: (get)')
    assert CACHE.send('get', HEADER)[1] == 'test data'


def test_cache_status():  # pragma: no cover
    print('TEST: (status)')
    assert type(CACHE.send('status')[1]) == dict
    assert list(CACHE.send('status')[1].keys()) == [
        'psize',
        'depth',
        'branch_pages',
        'leaf_pages',
        'overflow_pages',
        'entries'
        ]


def test_cache_info():  # pragma: no cover
    print('TEST: (info)')
    assert type(CACHE.send('info')[1]) == dict
    assert list(CACHE.send('info')[1].keys()) == [
        'map_addr',
        'map_size',
        'last_pgno',
        'last_txnid',
        'max_readers',
        'num_readers'
        ]


def test_cache_stale():  # pragma: no cover
    print('TEST: (stale)')
    assert type(CACHE.send('stale_readers')[1]) == int


def test_cache_readers():  # pragma: no cover
    print('TEST: (path)')
    assert CACHE.send('path')[1] == CACHE_PATH


def test_cache_locks():  # pragma: no cover
    print('TEST: (locks)')
    assert type(CACHE.send('locks')[1]) == str


# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':  # pragma: no cover
    test_cache_check()
    test_cache_set()
    test_cache_get()
    test_cache_status()
    test_cache_info()
    test_cache_stale()
    test_cache_readers()
    test_cache_locks()
