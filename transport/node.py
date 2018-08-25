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
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
                )
            )
        )
    )
from transport.conf.configuration import TASK_WORKERS
from transport.conf.configuration import LOG_LEVEL
from common.datatypes import *
from common.print_helpers import Logger
from tasks import *
import zmq
import lmdb

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)
VERSION                 = b'0.1'

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
            LOG.logc('NODE', 'start', '<---- received', 1, 'PURPLE')
            if envelope.lifespan > 0:
                envelope = self.run(envelope)
            self.send(envelope)

class TaskNode(Node):
    """
    NAME:           TaskNode

    DESCRIPTION:    A task variant of the node, whose role is to execute 
                    functions from the registry.

    METHODS:        .run(envelope)
                    Run a specific function from the registry. Which function is 
                    determined by the state of the pipeline.
    """
    def __init__(self, relay, recv_port, send_port, pid, functions):
        super(TaskNode, self).__init__(pid=pid, functions=functions)
        self.recv_socket = self._context.socket(zmq.PULL)
        self.send_socket = self._context.socket(zmq.PUSH)
        self.recv_socket.connect('tcp://{0}:{1}'.format(relay, recv_port))
        self.send_socket.connect('tcp://{0}:{1}'.format(relay, send_port))
        self.type = 'TASK'
        LOG.logc('TASK-{0}'.format(self.pid), 'Startup', 'Online', 0, 'GREEN')

    def run(self, envelope):
        header, meta, pipeline, data = envelope.unpack()
        func = pipeline.consume()
        kwargs = pipeline.extract()
        kwargs['data'] = data
        kwargs['worker'] = self.pid
        try:
            r = eval(self.functions[func])(kwargs)
        except Exception as e:
            raise Exception(e)
        envelope.pack(header, meta.extract(), pipeline.extract(), r)
        return envelope

class CacheNode(Node):
    """
    NAME:           CacheNode

    DESCRIPTION:    A cache variant of the node, whose role is to cache values.

    METHODS:        .store(key, value)
                    Store a key and value in the cache.

                    .retrieve(key)
                    Retrieve a value from the cache based on its key.

                    .run(envelope)
                    Run the cache request against the cache.
    """
    def __init__(self, host, port, pid):
        super(CacheNode, self).__init__(pid=pid)
        self.recv_socket = self._context.socket(zmq.ROUTER)
        self.recv_socket.bind('tcp://{0}:{1}'.format(host, port))
        self.send_socket = self.recv_socket
        self.type = 'CACHE'
        cwd = os.getcwd()
        cache_path = '{0}/transport/cache/'.format(cwd)
        print(cache_path)
        mylmdb = lmdb.Environment(
            path=cache_path,
            map_size=1000000000,
            subdir=True,
            map_async=True,
            writemap=True,
            max_readers=TASK_WORKERS,
            max_dbs=0,
            max_spare_txns=TASK_WORKERS,
            lock=True
        )
        self.lmdb = mylmdb
        LOG.logc('CACHE-{0}'.format(self.pid), 'Startup', 'Online', 0, 'GREEN')

    def store(self, key, value):
        with lmdb.Environment.begin(self.lmdb, write=True) as txn:
            txn.put(
                key,
                value,
                overwrite=True
                )

    def retrieve(self, key):
        with lmdb.Environment.begin(self.lmdb, write=True) as txn:
            return txn.get(key)

    def run(self, envelope):
        """
        Need to update to use the envelope standard
        """
        req = Tools.deserialize(cr[2])
        key = Tools.deserialize(cr[3])
        if req == 'check':
            try:
                r = self.cache_key_get(key.encode())
                if r != None:
                    return Tools.serialize(True)
                else:
                    return Tools.serialize(False)
            except Exception as e:
                LOG.loge('CACHE-{0}'.format(self.pid), 'check', e)
                return Tools.serialize(False)
        elif req == 'get':
            return self.cache_key_get(key.encode())
        elif req == 'set':
            try:
                self.cache_key_set(key.encode(), cr[4])
                return Tools.serialize(True)
            except Exception as e:
                LOG.loge('CACHE-{0}'.format(self.pid), 'set', e)
                return Tools.serialize(False)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
