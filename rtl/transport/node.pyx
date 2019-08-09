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
#                   numpy
#                   libcpp.string
#                   libcpp.uint_fast16_t
#
# Imports
# ------------------------------------------------------------------------ 79->
DEF GPU = 0

# Python imports
IF GPU == 1:
    import cupy as p
ELSE:
    import numpy as p
import os
import zmq
import lmdb
import cbor
import time
from os import getpid
from bokeh.server.server import Server
from rtl.tasks import *
import rtl.tasks as Tasks
from collections import deque
from numpy import frombuffer
from subprocess import check_output
from rtl.common.datatypes cimport Envelope
from rtl.transport.cache import ExperimentalCache
from rtl.transport.conf.configuration import TASK_WORKERS
from rtl.transport.conf.configuration import CACHE_PATH
from rtl.transport.conf.configuration import CACHE_MAP_SIZE
from rtl.transport.conf.configuration import RELAY_ADDR
from rtl.transport.conf.configuration import RELAY_SEND
from rtl.transport.conf.configuration import RELAY_RECV
from rtl.transport.conf.configuration import CACHE_LISTEN
from rtl.transport.conf.configuration import CACHE_RECV
from rtl.transport.conf.configuration import PLOT_LISTEN
from rtl.transport.conf.configuration import PLOT_ADDR
from rtl.transport.conf.configuration import DEBUG
from rtl.transport.conf.configuration import PROFILE
from rtl.transport.conf.configuration import PIDFILES
from rtl.common.print_helpers import printc, Colours
from rtl.web.plot import modify_doc
import time

cimport cython
# Cython imports
from numpy cimport ndarray
from libcpp.string cimport string
from libc.stdint cimport uint_fast16_t

# Globals
# ------------------------------------------------------------------------ 79->
RUNDIR = os.path.expanduser(PIDFILES)
COLOURS = Colours()
VERSION = '2.0a'

# Classes
# ------------------------------------------------------------------------ 79->


cdef class Node:
    """
    NAME:           Node

    DESCRIPTION:    Base class for transport nodes.

    METHODS:        .recv()
                    Receive sealed envelope from relay and returns an Envelope()
                    object.

                    .send(envelope)
                    Sends a sealed envelope to the relay.

                    .start()
                    Starts the node and begins requesting sealed envelopes.
    """

    def __init__(self):
        self.pid = getpid()
        self._context = zmq.Context()
        self.recv_poller = zmq.Poller()
        self.version = VERSION.encode()
        self.header = 'NODE-{0}'.format(self.pid).encode()
        command = ['cat', '/proc/sys/kernel/random/boot_id']
        self.domain_id = check_output(command).decode().rstrip('\n').encode()
        self.envelope = Envelope()
        self.cache = ExperimentalCache()

    cdef void recv(self):
        if DEBUG: print('NODE: recv')
        self.envelope.load(self.recv_socket.recv_multipart(copy=False))

    cdef void send(self):
        if DEBUG: print('NODE: send')
        if PROFILE: print('TS', time.time())
        self.send_socket.send_multipart(self.envelope.seal(), copy=False)

    cpdef void start(self):
        if DEBUG: print('NODE: start')
        while True:
            messages = dict(self.recv_poller.poll(5000))
            if self.recv_socket in messages and messages[self.recv_socket] == zmq.POLLIN:
                if PROFILE: print('TR', time.time())
                self.recv()
                if DEBUG: print('NODE: received envelope')
                if self.envelope.getLifespan() > 0:
                    self.run()
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

    def __init__(self, functions=''):
        super(TaskNode, self).__init__()
        self.header = 'TASK-{0}'.format(self.pid).encode()
        with open('{0}{1}'.format(RUNDIR, self.header.decode()), 'w+') as f:
            f.write(str(self.pid))
        if DEBUG: print('PIDLOC:', RUNDIR)
        self.recv_socket = self._context.socket(zmq.PULL)
        self.send_socket = self._context.socket(zmq.PUSH)
        pull_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_SEND)
        push_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_RECV)
        self.recv_socket.connect(pull_uri)
        self.send_socket.connect(push_uri)
        self.recv_poller.register(self.recv_socket, zmq.POLLIN)
        self.functions = functions
        self.jobQueue = deque()

    cdef void populateJobQueue(self, bytes id):
        if DEBUG: print('TASKNODE: populateJobQueue')
        cdef:
            dict schema
            long l
            long i
            list keys

        schema = cbor.loads(self.cache.get(id)[1])
        keys = list(schema.keys())
        l = len(keys)
        for i in range(l):
            self.jobQueue.append({keys[i]: schema[keys[i]]})

    cpdef void run(self):
        if DEBUG: print('TASKNODE: run')
        cdef:
            ndarray contents = self.envelope.getContents()
            bytes id = self.envelope.getId()
            str func
            str functionKey
            Exception msg
            double t
            dict job

        try:
            self.populateJobQueue(id)
            while self.jobQueue:
                t = time.perf_counter()
                job = self.jobQueue.popleft()
                functionKey = list(job.keys())[0]
                func = self.functions[functionKey]
                printc('Running: {0}'.format(func.split('.')[0]), COLOURS.LIGHTBLUE)
                contents = eval(func)(job[functionKey], contents)
                printc('Completed: {0} {1}'.format(
                    convert_time(time.perf_counter() - t), func.split('.')[0]), 
                    COLOURS.GREEN
                )
        except Exception as e:
            msg = Exception(
                'TASK-EVAL: {0}, {1}'.format(e)
                )
            print(msg)
            raise msg
        else:
            self.envelope.consume()
        self.envelope.setContents(contents)


cdef class PlotNode(Node):
    """
    NAME:           PlotNode

    DESCRIPTION:    A node running a bokeh server

    METHODS:        
    """

    def __init__(self, docs=''):
        super(PlotNode, self).__init__()
        self.header = 'PLOT-{0}'.format(self.pid).encode()
        self.server = Server(
            {'/': modify_doc}, 
            num_procs=1, 
            address=PLOT_ADDR,
            port=PLOT_LISTEN,
            allow_websocket_origin=["*"]
            )
        with open('{0}{1}'.format(RUNDIR, self.header.decode()), 'w+') as f:
            f.write(str(self.pid))
        if DEBUG: print('PIDLOC:', RUNDIR)

    cpdef void start(self):
        if DEBUG: print('PLOTNODE: start')
        self.server.io_loop.add_callback(self.server.show, "/")
        self.server.io_loop.start()
        try:
            self.server.start()
        except Exception as e:
            msg = Exception(
                'PLOT-ERROR: {0}'.format(e)
                )
            (msg)
            raise msg


cdef class CacheNode(Node):
    """
    NAME:           CacheNode

    DESCRIPTION:    A cache variant of the node, whose role is to initialize
                    the cache databse.

    METHODS:        .load_database()
                    Initialize the lmdb database environment.
    """

    def __init__(self, functions=''):
        super(CacheNode, self).__init__()
        self.header = 'CACHE-{0}'.format(self.pid).encode()
        with open('{0}{1}'.format(RUNDIR, self.header.decode()), 'w+') as f:
            f.write(str(self.pid))
        if DEBUG: print('PIDLOC:', RUNDIR)
        self.recv_socket = self._context.socket(zmq.ROUTER)
        router_uri = 'tcp://{0}:{1}'.format(CACHE_LISTEN, CACHE_RECV)
        self.recv_socket.bind(router_uri)
        self.load_database()

    cpdef void load_database(self):
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
cdef str convert_time(number):
    number = number * 1000
    return '{0:.2f} ms'.format(number)

# Main
# ------------------------------------------------------------------------ 79->
