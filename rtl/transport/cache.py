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
# Dependancies:
#

# Imports
# ------------------------------------------------------------------------ 79->
from transport.conf.configuration import CACHE_ADDR
from transport.conf.configuration import CACHE_RECV
from transport.conf.configuration import DEBUG
from transport.conf.configuration import CACHE_MAP_SIZE
from transport.conf.configuration import CACHE_PATH
from transport.conf.configuration import PROFILE
from transport.conf.configuration import TASK_WORKERS
import zmq
import lmdb
import cbor

# Globals
# ------------------------------------------------------------------------ 79->
VERSION = '0.4'

# Classes
# ------------------------------------------------------------------------ 79->

class ExperimentalCache(object):
    """
    NAME:           ExperimentalCache

    DESCRIPTION:    Sends cache requests to a local cache.

    METHODS:        .log_wrapper(msg, mode=0, colour='GREEN')
                    Wrapper for logger to clean up code.

                    .get(key)
                    Retreive a value from cache, or return None.

                    .put(key, value)
                    Add a value to the cache

                    .delete(key)
                    Attempt to delete a key.

                    .drop()
                    Attempt to drop the database.

                    .sync()
                    Force sync of the lmdb environment.

                    .status()
                    Return status information about the database environment.

                    .info()
                    Return additional information about the database.
    """
    
    def __init__(self):
        self.lmdb = lmdb.open(
            CACHE_PATH,
            # readonly=True,
            metasync=True,
            sync=True,
            writemap=True,
            readahead=True,
            subdir=True,
            map_size=CACHE_MAP_SIZE,
            lock=True,
            max_readers=TASK_WORKERS+2,
            max_dbs=0,
            max_spare_txns=TASK_WORKERS+2
            )

    def get(self, key):
        with self.lmdb.begin() as txn:
            r = txn.get(key)
        if r is None:
            return (key, False)
        return (key, r)

    def put(self, key, value):
        with self.lmdb.begin(write=True) as txn:
            r = txn.put(
                key,
                value,
                overwrite=True
            )
        return (key, r)

    def delete(self, key):
        with self.lmdb.begin(write=True) as txn:
            r = txn.delete(key.encode())
        return (key, r)

    def drop(self):
        with self.lmdb.begin(write=True) as txn:
            self.lmdb.drop(self.lmdb, delete=True)
    
    def status(self):
        return self.lmdb.stat()

    def info(self):
        return self.lmdb.info()

    def sync(self):
        return self.lmdb.sync()


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
