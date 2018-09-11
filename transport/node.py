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
from transport.conf.configuration import CACHED
from transport.conf.configuration import PROFILE
from common.datatypes import *
from common.encoding import Tools
from common.print_helpers import Logger
from common.print_helpers import timer
import subprocess
from tasks import *
import zmq
import lmdb
import time
import os

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)
VERSION = '0.4'

# Classes
# ------------------------------------------------------------------------ 79->


class Node(object):
    """
    NAME:           Node

    DESCRIPTION:    Base class for transport nodes.

    METHODS:        .log_wrapper(msg, mode=0, colour='GREEN')
                    Wrapper for logger to clean up code.

                    .recv()
                    Receive sealed envelop from relay and returns an Envelope()
                    object.

                    .send(envelope)
                    Sends a sealed envelope to the relay.

                    .consume(pipeline)
                    Pull a task off the pipeline.

                    .start()
                    Starts the node and begins requesting sealed envelopes.
    """

    @timer(LOG, 'node', PROFILE)
    def __init__(self):
        super(Node, self).__init__()
        self.pid = os.getpid()
        self.log_msg = {
            'system': 'node-{0}'.format(self.pid),
            'name': self.__init__.__name__,
            }
        self._context = zmq.Context()
        self.version = VERSION
        self.header = 'NODE-{0}'.format(self.pid)
        command = ['cat', '/proc/sys/kernel/random/boot_id']
        self.domain_id = subprocess.check_output(command).decode().rstrip('\n')
        self.envelope = Envelope(cached=False)

    def log_wrapper(self, msg, mode=0, colour='GREEN'):
        self.log_msg['message'] = msg
        self.log_msg['colour'] = colour
        LOG.logw(self.log_msg, mode, 'machine.log')

    @timer(LOG, 'node', PROFILE)
    def recv_loop(self):
        return self.recv_socket.recv_multipart()

    @timer(LOG, 'node', PROFILE)
    def load_envelope(self, r):
        self.envelope.load(r)

    @timer(LOG, 'node', PROFILE)
    def send(self):
        self.send_socket.send_multipart(self.envelope.seal())

    @timer(LOG, 'node', PROFILE)
    def consume(self, pipeline):
        current = pipeline['tasks'].pop(0)
        pipeline['completed'].append(current)
        return current

    @timer(LOG, 'node', PROFILE)
    def start(self):
        self.log_msg['name'] = self.start.__name__
        while True:
            r = self.recv_loop()
            self.load_envelope(r)
            self.log_wrapper('<---- received', mode=2, colour='PURPLE')
            if self.envelope.get_lifespan() > 0:
                self.run()
            self.send()
            self.log_wrapper('sent ---->', mode=2, colour='PURPLE')


class TaskNode(Node):
    """
    NAME:           TaskNode

    DESCRIPTION:    A task variant of the node, whose role is to execute
                    functions from the registry.

    METHODS:        .run(envelope)
                    Run a specific function from the registry. Which function
                    is determined by the state of the pipeline.
    """

    @timer(LOG, 'tasknode', PROFILE)
    def __init__(self, functions=''):
        super(TaskNode, self).__init__()
        self.log_msg = {
            'system': 'tasknode-{0}'.format(self.pid),
            'name': self.__init__.__name__,
            }
        with open('var/run/{0}'.format(self.log_msg['system']), 'w+') as f:
            f.write(str(self.pid))
        self.recv_socket = self._context.socket(zmq.PULL)
        self.send_socket = self._context.socket(zmq.PUSH)
        pull_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_SEND)
        push_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_RECV)
        self.recv_socket.connect(pull_uri)
        self.send_socket.connect(push_uri)
        self.functions = functions
        self.type = 'TASK'
        self.header = 'TASK-{0}'.format(self.pid)
        msg = 'online-domain({0})'.format(self.domain_id)
        self.log_wrapper(msg, mode=0)

    @timer(LOG, 'tasknode', PROFILE)
    def run(self):
        self.log_msg['name'] = self.run.__name__
        pipeline = self.envelope.get_pipeline()
        pipeline['data'] = self.envelope.get_data()
        pipeline['worker'] = self.pid
        self.log_wrapper(pipeline['tasks'][0], mode=0)
        try:
            f = eval(self.functions[self.consume(pipeline)])
            r = f(pipeline)
        except Exception as e:
            raise Exception('TASK-EVAL: {0}'.format(e))
        self.envelope.data = r


class CacheNode(Node):
    """
    NAME:           CacheNode

    DESCRIPTION:    A cache variant of the node, whose role is to initialize
                    the cache databse.

    METHODS:        .load_database()
                    Initialize the lmdb database environment.
    """

    @timer(LOG, 'cachenode', PROFILE)
    def __init__(self, functions=''):
        super(CacheNode, self).__init__()
        self.log_msg = {
            'system': 'cachenode-{0}'.format(self.pid),
            'name': self.__init__.__name__,
            }
        with open('var/run/{0}'.format(self.log_msg['system']), 'w+') as f:
            f.write(str(self.pid))
        self.recv_socket = self._context.socket(zmq.ROUTER)
        router_uri = 'tcp://{0}:{1}'.format(CACHE_LISTEN, CACHE_RECV)
        self.recv_socket.bind(router_uri)
        self.type = 'CACHE'
        self.count = 1
        self.header = 'CACHE-{0}'.format(self.pid)
        self.load_database()

    @timer(LOG, 'cachenode', PROFILE)
    def load_database(self):
        self.lmdb = lmdb.Environment(
            path=CACHE_PATH,
            map_size=CACHE_MAP_SIZE,
            subdir=True,
            readonly=False,
            metasync=True,
            # map_async=True,
            sync=True,
            writemap=True,
            readahead=True,
            max_readers=TASK_WORKERS+2,
            max_dbs=0,
            max_spare_txns=TASK_WORKERS+2,
            lock=True,
            create=True
        )


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
