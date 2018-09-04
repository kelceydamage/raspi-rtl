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
#                   zmq
#                   lmdb
#                   tasks
#                   common
#
# Imports
# ------------------------------------------------------------------------ 79->
import os
from transport.conf.configuration import TASK_WORKERS
from transport.conf.configuration import LOG_LEVEL
from transport.conf.configuration import CACHE_PATH
from transport.conf.configuration import CACHE_MAP_SIZE
from transport.conf.configuration import RELAY_ADDR
from transport.conf.configuration import RELAY_SEND
from transport.conf.configuration import RELAY_RECV
from transport.conf.configuration import CACHE_LISTEN
from transport.conf.configuration import CACHE_RECV
from common.datatypes import *
from common.print_helpers import Logger
from tasks import *
import zmq
import lmdb

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)
VERSION = b'0.2'

# Classes
# ------------------------------------------------------------------------ 79->


class Node(object):
    """
    NAME:           Node

    DESCRIPTION:    Base class for transport nodes.

    METHODS:        .recv()
                    Receive sealed envelop from relay and returns an Envelope()
                    object.

                    .send(envelope)
                    Sends a sealed envelope to the relay.

                    .start()
                    Starts the node and begins requesting sealed envelopes.
    """

    def __init__(self, pid, functions=''):
        super(Node, self).__init__()
        self._context = zmq.Context()
        self.version = VERSION
        self.pid = pid
        self.header = 'NODE-{0}'.format(self.pid)
        self.functions = functions

    def recv(self):
        envelope = Envelope()
        envelope.load(self.recv_socket.recv_multipart())
        return envelope

    def send(self, envelope):
        self.send_socket.send_multipart(envelope.seal())

    def start(self):
        while True:
            envelope = self.recv()
            LOG.logc(self.header, 'start', '<---- received', 3, 'PURPLE')
            if envelope.lifespan > 0:
                envelope = self.run(envelope)
            self.send(envelope)


class TaskNode(Node):
    """
    NAME:           TaskNode

    DESCRIPTION:    A task variant of the node, whose role is to execute
                    functions from the registry.

    METHODS:        .run(envelope)
                    Run a specific function from the registry. Which function
                    is determined by the state of the pipeline.
    """

    def __init__(self, pid, functions):
        super(TaskNode, self).__init__(pid=pid, functions=functions)
        self.recv_socket = self._context.socket(zmq.PULL)
        self.send_socket = self._context.socket(zmq.PUSH)
        pull_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_SEND)
        push_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_RECV)
        self.recv_socket.connect(pull_uri)
        self.send_socket.connect(push_uri)
        self.type = 'TASK'
        self.header = 'TASK-{0}'.format(self.pid)
        LOG.logc(self.header, 'Startup', 'Online', 0, 'GREEN')

    def run(self, envelope):
        header, meta, pipeline, data = envelope.unpack()
        func = pipeline.consume()
        kwargs = pipeline.extract()
        kwargs['data'] = data
        kwargs['worker'] = self.pid
        try:
            f = eval(self.functions[func])
            r = f(kwargs)
        except Exception as e:
            raise Exception('TASK-EVAL: {0}'.format(e))
        envelope.pack(header, meta.extract(), pipeline.extract(), r)
        return envelope


class CacheNode(Node):
    """
    NAME:           CacheNode

    DESCRIPTION:    A cache variant of the node, whose role is to cache values.

    METHODS:        .load_database()
                    Initialize the lmdb database environment.

                    .recv()
                    Receive incoming envelopes.

                    .send()
                    Send outgoing envelope.

                    .handler(func, key=None, value=None)
                    Handle all incoming requests and run requested method.

                    .store(key, value)
                    Store a key and value in the cache.

                    .retrieve(key)
                    Retrieve a value from the cache based on its key.

                    .check(key)
                    Check if a key exists in the database.

                    .sync()
                    Force sync of the lmdb environment.

                    .get_status()
                    Return status information about the database environment.

                    .get_info()
                    Return additional information about the database.

                    .get_path()
                    Return the location of the database.

                    .get_stale_readers()
                    Return a count of stale reader connections.

                    .get_reader_lock_table()
                    Return lock table.

                    .run(envelope)
                    Run the cache request against the cache.
    """

    def __init__(self, pid):
        super(CacheNode, self).__init__(pid=pid)
        self.recv_socket = self._context.socket(zmq.ROUTER)
        router_uri = 'tcp://{0}:{1}'.format(CACHE_LISTEN, CACHE_RECV)
        self.recv_socket.bind(router_uri)
        self.type = 'CACHE'
        self.count = 0
        self.header = 'CACHE-{0}'.format(self.pid)
        self.load_database()
        self.methods = {
            'status': self.get_status,
            'check': self.check,
            'get': self.retrieve,
            'set': self.store,
            'info': self.get_info,
            'path': self.get_path,
            'stale_readers': self.get_stale_readers,
            'locks': self.get_reader_lock_table
        }
        LOG.logc(self.header, 'Startup', 'Online', 0, 'GREEN')

    def load_database(self):
        self.lmdb = lmdb.Environment(
            path=CACHE_PATH,
            map_size=CACHE_MAP_SIZE,
            subdir=True,
            readonly=False,
            metasync=False,
            map_async=True,
            sync=False,
            writemap=True,
            readahead=True,
            max_readers=TASK_WORKERS*2,
            max_dbs=0,
            max_spare_txns=TASK_WORKERS*2,
            lock=True,
            create=True
        )

    def recv(self):
        parcel = Parcel()
        parcel.load(self.recv_socket.recv_multipart())
        route, envelope = parcel.unpack()
        self.current_route = route
        return envelope

    def send(self, envelope):
        parcel = Parcel()
        parcel.pack(self.current_route, envelope)
        self.recv_socket.send_multipart(parcel.seal())
        self.current_route = ''

    def handler(self, func, key=None, value=None):
        try:
            if value is not None:
                return func(key.encode(), Tools.serialize(value))
            elif key is not None:
                return func(key.encode())
            else:
                return func()
        except Exception as e:
            LOG.loge(self.header, func.__name__, e)
            return False

    def store(self, key, value):
        with lmdb.Environment.begin(self.lmdb, write=True) as txn:
            txn.put(key, value, overwrite=True)
            self.count += 1
        return True

    def retrieve(self, key):
        with lmdb.Environment.begin(self.lmdb) as txn:
            value = txn.get(key)
        return value

    def check(self, key):
        if self.retrieve(key) is None:
            return False
        else:
            return True

    def sync(self):
        self.lmdb.sync()

    def get_status(self):
        return self.lmdb.stat()

    def get_info(self):
        return self.lmdb.info()

    def get_path(self):
        return self.lmdb.path()

    def get_stale_readers(self):
        return self.lmdb.reader_check()

    def get_reader_lock_table(self):
        return self.lmdb.readers()

    def run(self, envelope):
        LOG.logc(self.header, 'run', '<---- request', 3, 'PURPLE')
        key, value = envelope.get_data()
        response = [key]
        request = envelope.get_raw_header()
        value = self.handler(self.methods[request], key, value)
        if isinstance(value, bytes):
            value = Tools.deserialize(value)
        envelope.update_data([key, value])
        if self.count % 10000 == 0:
            print('CACHE VOLUME:', self.count)
        return envelope


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
