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
#                   conf
#                   common
#                   zmq
#
# Imports
# ------------------------------------------------------------------------ 79->

# Python imports
import zmq
import os
import math
from numpy import array_split
from numpy import empty
from transport.conf.configuration import CHUNKING_SIZE
from transport.conf.configuration import RELAY_LISTEN
from transport.conf.configuration import RELAY_RECV
from transport.conf.configuration import RELAY_SEND
from transport.conf.configuration import RELAY_PUBLISHER

# Cython imports
cimport cython
from numpy cimport ndarray
from common.datatypes cimport Envelope
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast16_t

# Globals
# ------------------------------------------------------------------------ 79->

VERSION = '2.0a'

# Classes
# ------------------------------------------------------------------------ 79->


cdef class Relay:
    """
    NAME:           Router {0}

    DESCRIPTION:    Routes messages to available workers.

    METHODS:        .send(header, meta, pipeline)
                    Send the envelope to a node.

                    .recv_loop()
                    Receive sealed envelop returns an Envelope()
                    object.

                    .create_state(meta)
                    Store the current envelope stage in state.

                    .retrieve_state(meta)
                    Retrieve and decrement the state for a given stage.

                    .assemble(envelope)
                    Compile all outstanding components of a stage and publish.

                    .chunk(envelope)
                    If an envelope's data exceeds the chunking threshold,
                    split the envelope into multiple envelopes and push to
                    the nodes.

                    .start()
                    Start the relay and begin listening.
    """.format(VERSION)

    def __cinit__(self, functions=''):
        cdef:
            str pull_uri
            str push_uri
            str publiser_uri

        self.version = VERSION.encode()
        self.chunk_size = <long>CHUNKING_SIZE
        self.assembly_buffer = {}
        self.index_tracker = {}
        self.success = True
        self.pid = os.getpid()
        with open('var/run/{0}'.format('relay-{0}'.format(self.pid)), 'w+') as f:
            f.write(str(self.pid))
        context = zmq.Context()
        self.recv_socket = context.socket(zmq.PULL)
        self.send_socket = context.socket(zmq.PUSH)
        self.publisher = context.socket(zmq.PUB)
        pull_uri = 'tcp://{0}:{1}'.format(RELAY_LISTEN, RELAY_RECV)
        push_uri = 'tcp://{0}:{1}'.format(RELAY_LISTEN, RELAY_SEND)
        publiser_uri = 'tcp://{0}:{1}'.format(RELAY_LISTEN, RELAY_PUBLISHER)
        self.recv_socket.bind(pull_uri)
        self.send_socket.bind(push_uri)
        self.publisher.bind(publiser_uri)
        self.envelope = <Envelope>Envelope()

    cdef void send(self):
        self.send_socket.send_multipart(self.envelope.seal())

    cdef void publish(self):
        self.publisher.send_multipart(self.envelope.seal())

    cdef void recv_loop(self):
        self.envelope.load(self.recv_socket.recv_multipart())

    cdef void create_state(self, string header, long length):
        if self.state.find(header) != self.state.end():
            self.state[header] += 1
        else:
            self.state[header] = 1

    cdef long retrieve_state(self, string header):
        if self.state.find(header) != self.state.end():
            self.state[header] -= 1
            if self.state[header] == 0:
                self.state.erase(header)
                return 0
            return self.state[header]
        self.success = False
        return 0

    cdef long assemble(self) except -1:
        cdef:
            long i
            long length
            string h = self.envelope.get_header()
            long count = self.retrieve_state(h)

        if self.success:
            self.chunk_holder = self.envelope.get_ndata()
            length = <long>len(self.chunk_holder)
            for i in range(length):
                self.assembly_buffer[h][self.index_tracker[h] + i] = self.chunk_holder[i]
            self.index_tracker[h] += length
            if count == 0:
                self.envelope.set_ndata(self.assembly_buffer[h])
                self.publish()
                del self.index_tracker[h]
                del self.assembly_buffer[h]
        else:
            self.publish()
        return 0

    cdef long chunk(self) except -1:
        cdef:
            long i
            string h = self.envelope.get_header()
            long length = self.envelope.get_length()
            long groups = math.ceil(
                self.envelope.get_length() / float(self.chunk_size)
                )

        if length <= 1 or length <= self.chunk_size:
            self.send()
        else:
            self.chunk_buffer = array_split(
                self.envelope.get_ndata(), 
                groups, 
                axis=0
                )
            self.assembly_buffer[h] = empty(
                (len(self.chunk_buffer[0]) * groups, 
                len(self.chunk_buffer[0][0]))
                )
            self.index_tracker[h] = 0
            for i in range(groups):
                self.envelope.set_ndata(self.chunk_buffer[i])
                self.create_state(h, length)
                self.send()
        return 0

    cpdef void start(self):
        cdef: 
            long r

        while True:
            self.recv_loop()
            if self.envelope.get_lifespan() > 0:
                r = self.chunk()
                if r == -1:
                    raise
            else:
                r = self.assemble()
                if r == -1:
                    raise

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
