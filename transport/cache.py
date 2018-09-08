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
from transport.conf.configuration import LOG_LEVEL
from transport.conf.configuration import CACHE_MAP_SIZE
from transport.conf.configuration import CACHE_PATH
from transport.conf.configuration import PROFILE
from common.print_helpers import Logger
from common.print_helpers import timer
from common.encoding import Tools
import zmq
import lmdb

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)
VERSION = '0.3'

# Classes
# ------------------------------------------------------------------------ 79->


class Cache(object):
    """
    NAME:           Cache

    DESCRIPTION:    Sends cache requests to a cache node.

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

    @timer(LOG, 'cache', PROFILE)
    def __init__(self):
        self.log_msg = {
                'system': 'cache',
                'name': self.__init__.__name__,
            }
        context = zmq.Context()
        try:
            req_uri = 'tcp://{0}:{1}'.format(CACHE_ADDR, CACHE_RECV)
            self.req_socket = context.socket(zmq.REQ)
            self.req_socket.connect(req_uri)
            self.lmdb = lmdb.open(
                CACHE_PATH,
                # readonly=True,
                subdir=True,
                map_size=CACHE_MAP_SIZE,
                lock=True
                )
        except Exception as e:
            self.log_wrapper(str(e), mode=0)

    def log_wrapper(self, msg, mode=0, colour='GREEN'):
        self.log_msg['message'] = msg
        self.log_msg['colour'] = colour
        LOG.logw(self.log_msg, mode, 'machine.log')

    @timer(LOG, 'cache', PROFILE)
    def get(self, key):
        with self.lmdb.begin() as txn:
            r = txn.get(key.encode())
        if r is None:
            return (key, False)
        return (key, Tools.deserialize(r))

    @timer(LOG, 'cache', PROFILE)
    def put(self, key, value):
        try:
            with self.lmdb.begin(write=True) as txn:
                r = txn.put(
                    key.encode(),
                    Tools.serialize(value),
                    overwrite=True
                    )
        except Exception as e:
            raise Exception(e)
        else:
            return (key, r)

    @timer(LOG, 'cache', PROFILE)
    def delete(self, key):
        with self.lmdb.begin(write=True) as txn:
            r = txn.delete(key.encode())
        return (key, r)

    @timer(LOG, 'cache', PROFILE)
    def drop(self):
        with self.lmdb.begin(write=True) as txn:
            self.lmdb.drop(self.lmdb, delete=True)

    @timer(LOG, 'cache', PROFILE)
    def sync(self):
        return self.lmdb.sync()

    @timer(LOG, 'cache', PROFILE)
    def status(self):
        return self.lmdb.stat()

    @timer(LOG, 'cache', PROFILE)
    def info(self):
        return self.lmdb.info()

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
