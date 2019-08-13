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
This module provides a cache interface for accessing LMDB.

Note:
    this is not intended for general cache use and is intended for job meta
    data caching.

Todo
    - Convert to cython

"""


# Imports
# ------------------------------------------------------------------------ 79->
import lmdb
from rtl.transport.conf.configuration import CACHE_MAP_SIZE
from rtl.transport.conf.configuration import CACHE_PATH
from rtl.transport.conf.configuration import TASK_WORKERS


# Classes
# ------------------------------------------------------------------------ 79->


class ExperimentalCache(object):
    """Experimental cache is an api abstraction for LMDB."""

    def __init__(self):
        """Initializer for the experimental cache class.

        There are non-passable paramaters used to open the cache. These are:
            * metasync=True
            * sync=True
            * writemap=True
            * readahead=True
            * subdir=True
            * Lock=True
            * max_dbs=true

        The following can be configured in :ref:`configuration`:
            * CACHE_PATH
            * CACHE_MAP_SIZE
            * TASK_WORKERS

        Note:
            Sets up the LMDB environment for use.

        """
        self.lmdb = lmdb.open(
            CACHE_PATH,
            metasync=True,
            sync=True,
            writemap=True,
            readahead=True,
            subdir=True,
            map_size=CACHE_MAP_SIZE,
            lock=True,
            max_readers=TASK_WORKERS+2,
            max_dbs=1,
            max_spare_txns=TASK_WORKERS+2
            )
        self.ndb = self.lmdb.open_db(b'raspi-rtl')

    def get(self, key):
        """Get method for retrieving a value from the cache based on a key.

        Example:
            .. code-block:: Python

                key, result = ExperimentalCache().get(my_key)

        Args:
            key (bytes): a key name encoded as bytes.

        Returns:
            tuple:
            - key (bytes): a key name encoded as bytes.
            - result (bool, bytes): a value encoded as bytes, or a boolean \
            false if not found.

        """
        with self.lmdb.begin() as txn:
            result = txn.get(key)
        if result is None:
            return (key, False)
        return (key, result)

    def put(self, key, value):
        """Put method for adding a value to the cache based on a key.

        Example:
            .. code-block:: Python

                key, result = ExperimentalCache().put(my_key, my_value)

        Args:
            key (bytes): a key name encoded as bytes.
            value (bytes): a value encoded as bytes.

        Returns:
            tuple:
            - key (bytes): a key name encoded as bytes.
            - result (bool): a boolean value for success.

        """
        with self.lmdb.begin(write=True) as txn:
            result = txn.put(
                key,
                value,
                overwrite=True
            )
        return (key, result)

    def delete(self, key):
        """Delete method for removing a value from the cache based on a key.

        Example:
            .. code-block:: Python

                key, result = ExperimentalCache().put(my_key)

        Args:
            key (bytes): a key name encoded as bytes.

        Returns:
            tuple:
            - key (bytes): a key name encoded as bytes.
            - result (bool): a boolean value for success.

        """
        with self.lmdb.begin(write=True) as txn:
            result = txn.delete(key)
        return (key, result)

    def status(self):
        """Status method for retrieving details on the makup of the cache.

        Example:
            .. code-block:: Python

                status = ExperimentalCache().status()

        Returns:
            dict:
            - psize (int)
            - depth (int)
            - branch_pages (int)
            - leaf_pages (int)
            - overflow_pages (int)
            - entries (int)

        """
        return self.lmdb.stat()

    def info(self):
        """Info method for retrieving details on the environment.

        Example:
            .. code-block:: Python

                info = ExperimentalCache().info()

        Returns:
            dict:
            - map_addr (int)
            - map_size (int)
            - last_pgno (int)
            - last_txnid (int)
            - max_readers (int)
            - num_readers (int)

        """
        return self.lmdb.info()

    def sync(self):
        """Sync the state of the cache

        Example:
            .. code-block:: Python

                ExperimentalCache().sync()

        """
        return self.lmdb.sync()


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
