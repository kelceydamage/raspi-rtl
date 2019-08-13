#! /usr/bin/env python
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
"""Pytest module for testing the rtl.transport.cache module."""


# Imports
# ------------------------------------------------------------------------ 79->
from rtl.transport.cache import ExperimentalCache


# Const
# ------------------------------------------------------------------------ 79->
CACHE = ExperimentalCache()


# Functions
# ------------------------------------------------------------------------ 79->
def test_cache_instantiation():
    """Test instantiating the experimental cache object"""
    cache = ExperimentalCache()
    assert isinstance(cache, ExperimentalCache)


def test_cache_put():
    """Test putting a value into the cache store"""
    result = CACHE.put(b'test', b'10')
    assert result == (b'test', True)


def test_cache_valid_get():
    """Test retrieving an value from the cache store"""
    result = CACHE.get(b'test')
    assert result == (b'test', b'10')


def test_cache_invalid_get():
    """Test retrieving an value that doesn't exist from teh cache store"""
    result = CACHE.get(b'bob')
    assert result == (b'bob', False)


def test_cache_delete():
    """Test deleting a value from the cache store"""
    result = CACHE.delete(b'test')
    assert result == (b'test', True)


def test_cache_status():
    """Test calling the cache status function"""
    result = CACHE.status()
    assert isinstance(result, dict)


def test_cache_info():
    """Test calling the cache info function"""
    result = CACHE.info()
    assert isinstance(result, dict)


def test_cache_sync():
    """Test flushing the system buffers to disk

    Note:
        This function is not used by default as the database is opened
        with sync=True. For certain high performance situations the cache
        may need to be opened with sync=Fasle, and doing so means all the
        data in it is volatile

    """
    result = CACHE.sync()
    assert result is None


# Main
# ------------------------------------------------------------------------ 79->
