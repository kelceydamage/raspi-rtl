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
#                   common
#                   conf
#
# Imports
# ------------------------------------------------------------------------ 79->
from transport.conf.configuration import RELAY_ADDR
from transport.conf.configuration import RELAY_RECV
from transport.conf.configuration import RELAY_PUBLISHER
from transport.conf.configuration import CACHE_ADDR
from transport.conf.configuration import CACHE_RECV
from transport.conf.configuration import LOG_LEVEL
from transport.conf.configuration import CACHE_MAP_SIZE
from transport.conf.configuration import CACHE_PATH
from transport.conf.configuration import PROFILE
from common.datatypes cimport Envelope
from common.print_helpers import Logger
from common.print_helpers import timer
import zmq
import lmdb
import time

cimport cython
from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.string cimport string
from libcpp.map cimport map
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast8_t
from libc.stdint cimport int_fast16_t
from libc.stdio cimport printf
from libc.stdlib cimport atoi
from posix cimport time as p_time

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)
VERSION = '0.4'

# Classes
# ------------------------------------------------------------------------ 79->


cdef class Dispatcher(object):
    """
    NAME:           Dispatcher

    DESCRIPTION:    Dispatches tasks to the relay.

    METHODS:        .log_wrapper(msg, mode=0, colour='GREEN')
                    Wrapper for logger to clean up code.

                    .send(envelope)
                    Send a type Envelope() object to the relay. This is a
                    blocking method, and will wait until the results of the
                    task are returned.

                    ._receive()
                    waits for the relay to publish the result. Returns the
                    result as an envelope(obj).

                    .close()
                    Close the connections to the relay.
    """

    cdef:
        object push_socket
        object sub_socket
        list results

    def __init__(self):
        context = zmq.Context()
        push_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_RECV)
        pull_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_PUBLISHER)
        self.push_socket = context.socket(zmq.PUSH)
        self.sub_socket = context.socket(zmq.SUB)
        self.push_socket.connect(push_uri)
        self.sub_socket.connect(pull_uri)
        self.results = []

    cpdef Envelope _recieve(self):
        envelope = Envelope()
        envelope.load(self.sub_socket.recv_multipart(), unseal=True)
        return envelope

    cpdef close(self):
        self.push_socket.disconnect(self.push_addr)
        self.sub_socket.disconnect(self.sub_addr)

    cdef Envelope _send(self, Envelope envelope):
        self.sub_socket.set(zmq.SUBSCRIBE, envelope.get_header())
        self.push_socket.send_multipart(envelope.seal())
        return self._recieve()

    cpdef Envelope send(self, Envelope envelope):
        return self._send(envelope)


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
