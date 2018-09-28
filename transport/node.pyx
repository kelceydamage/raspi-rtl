#!python
#cython: language_level=3, cdivision=True
###boundscheck=False, wraparound=False //(Disabled by default)
# ------------------------------------------------------------------------ 79->
# Author: Kelcey Damage
# Cython: 0.28+
# Doc
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
from common.datatypes cimport Envelope, Pipeline
from common.encoding import Tools
from common.print_helpers import Logger
from common.print_helpers import timer
import subprocess
from tasks import *
import ast
import zmq
import lmdb
import time
import os
import numpy as np

cimport numpy as np
cimport cython
from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.string cimport string
from libcpp.map cimport map
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast8_t, uint_fast16_t
from libc.stdint cimport int_fast16_t
from libc.stdio cimport printf
from libc.stdlib cimport atoi
from posix cimport time as p_time

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)
VERSION = b'0.4'

# Classes
# ------------------------------------------------------------------------ 79->


cdef class Node(object):
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

    cdef:
        uint_fast16_t pid
        dict log_msg
        Envelope envelope
        object _context
        string version
        string header
        string domain_id

    def __init__(self):
        super(Node, self).__init__()
        self.pid = os.getpid()
        self.log_msg = {
            'system': 'node-{0}'.format(self.pid),
            'name': self.__init__.__name__,
            }
        self._context = zmq.Context()
        self.version = VERSION
        self.header = 'NODE-{0}'.format(self.pid).encode()
        command = ['cat', '/proc/sys/kernel/random/boot_id']
        self.domain_id = subprocess.check_output(command).decode().rstrip('\n').encode()
        self.envelope = Envelope(cached=False)

    cdef log_wrapper(self, msg, mode=0, colour='GREEN'):
        self.log_msg['message'] = msg
        self.log_msg['colour'] = colour
        #LOG.logw(self.log_msg, mode, 'machine.log')

    cdef recv_loop(self):
        return self.recv_socket.recv_multipart()

    cdef load_envelope(self, r):
        self.envelope.load(r, unseal=True)

    cdef send(self):
        #print(self.envelope.header, len(self.envelope.data))
        self.send_socket.send_multipart(self.envelope.seal())

    cpdef start(self):
        self.log_msg['name'] = self.start.__name__
        while True:
            r = self.recv_loop()
            #print('N recv')
            #print('N recv1', self.envelope.header, len(r))
            self.load_envelope(r)
            #print('N-{0} recv2'.format(self.pid), self.envelope.header)
            if self.envelope.get_lifespan() > 0:
                #print('N run')
                self.run()
            #print('N send')
            #print('N send', self.envelope.header)
            self.send()


cdef class TaskNode(Node):
    """
    NAME:           TaskNode

    DESCRIPTION:    A task variant of the node, whose role is to execute
                    functions from the registry.

    METHODS:        .run(envelope)
                    Run a specific function from the registry. Which function
                    is determined by the state of the pipeline.
    """

    cdef:
        public object recv_socket
        public object send_socket
        public dict functions

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
        self.header = 'TASK-{0}'.format(self.pid).encode()
        msg = 'online-domain({0})'.format(self.domain_id)
        self.log_wrapper(msg, mode=0)

    cpdef void run(self):
        cdef np.ndarray r
        t = time.perf_counter()
        self.log_msg['name'] = 'run'
        self.log_wrapper(self.envelope.meta['tasks'][0], mode=0)
        #print('N data', len(self.envelope.data))
        try:
            f = eval(self.functions[self.envelope.meta['tasks'][0]])
            r = f(self.envelope.meta['kwargs'], np.frombuffer(self.envelope.data).reshape(self.envelope.get_length(), self.envelope.get_shape()))
            #print('N r', len(r))
        except Exception as e:
            print('TASK-EVAL: {0}, {1}'.format(self.envelope['completed'][-1], e))
            raise Exception('TASK-EVAL: {0}, {1}'.format(self.envelope['completed'][-1], e))
        else:
            self.envelope.consume()
        self.envelope.set_data(r)
        #print('N-{1} run {0:.8f}'.format(time.perf_counter() - t, self.pid))
        #print('N len', len(self.envelope.data))


cdef class CacheNode(Node):
    """
    NAME:           CacheNode

    DESCRIPTION:    A cache variant of the node, whose role is to initialize
                    the cache databse.

    METHODS:        .load_database()
                    Initialize the lmdb database environment.
    """

    cdef:
        public object recv_socket
        public object lmdb

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
        self.header = 'CACHE-{0}'.format(self.pid).encode()
        self.load_database()

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
