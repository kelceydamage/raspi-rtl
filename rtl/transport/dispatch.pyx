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

# Python imports
import zmq
import time
from rtl.transport.conf.configuration import RELAY_ADDR
from rtl.transport.conf.configuration import RELAY_RECV
from rtl.transport.conf.configuration import RELAY_PUBLISHER
from rtl.transport.conf.configuration import DEBUG
from rtl.transport.conf.configuration import PROFILE

# Cython imports
cimport cython
from rtl.common.datatypes cimport Envelope

# Globals
# ------------------------------------------------------------------------ 79->

VERSION = '2.0a'

# Classes
# ------------------------------------------------------------------------ 79->


cdef class Dispatcher:
    """
    NAME:           Dispatcher

    DESCRIPTION:    Dispatches tasks to the relay.

    METHODS:        .send()
                    Python wrapper for ._send()
                    
                    ._send(envelope)
                    Send a type Envelope() object to the relay. This is a
                    blocking method, and will wait until the results of the
                    task are returned.

                    ._receive()
                    waits for the relay to publish the result. Returns the
                    result as an envelope(obj).

                    .close()
                    Close the connections to the relay.
    """

    def __init__(self):
        context = zmq.Context()
        push_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_RECV)
        pull_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_PUBLISHER)
        self.push_socket = context.socket(zmq.PUSH)
        self.sub_socket = context.socket(zmq.SUB)
        self.push_socket.connect(push_uri)
        self.sub_socket.connect(pull_uri)
        self.results = []
        if DEBUG: print('DISPATCHER PUSH:', push_uri)
        if DEBUG: print('DISPATCHER SUB:', pull_uri)

    cdef Envelope _recieve(self):
        if DEBUG: print('DISPATCHER: _receive')
        envelope = Envelope()
        envelope.load(self.sub_socket.recv_multipart(copy=False))
        if PROFILE: print('DR', time.time())
        return envelope

    cdef void close(self):
        if DEBUG: print('DISPATCHER: close')
        self.push_socket.disconnect(self.push_addr)
        self.sub_socket.disconnect(self.sub_addr)

    cdef Envelope _send(self, Envelope envelope):
        if DEBUG: print('DISPATCHER: _send')
        self.sub_socket.set(zmq.SUBSCRIBE, envelope.getId())
        self.push_socket.send_multipart(envelope.seal(), copy=False)
        if PROFILE: print('DS', time.time())
        return self._recieve()

    cpdef Envelope send(self, Envelope envelope):
        if DEBUG: print('DISPATCHER: send')
        return self._send(envelope)


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
