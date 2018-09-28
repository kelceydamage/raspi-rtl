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
from transport.conf.configuration import CHUNKING_SIZE
from transport.conf.configuration import RELAY_LISTEN
from transport.conf.configuration import RELAY_RECV
from transport.conf.configuration import RELAY_SEND
from transport.conf.configuration import RELAY_PUBLISHER

import zmq
import os
import time
import math
import numpy as np

cimport cython
cimport numpy as np
from common.datatypes cimport Envelope
from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast16_t

# Globals
# ------------------------------------------------------------------------ 79->
VERSION = '0.4'

# Classes
# ------------------------------------------------------------------------ 79->


cdef class Relay:
    """
    NAME:           Router

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
    """

    cdef:
        uint_fast16_t pid
        long chunk_size
        list chunk_buffer
        #np.ndarray chunk_buffer
        bint success
        #list assembly_buffer
        dict assembly_buffer
        unordered_map[string, long] state
        object recv_socket
        object send_socket
        object publisher
        Envelope envelope
        dict index_tracker
        np.ndarray chunk_holder

    def __cinit__(self, functions=''):
        super(Relay, self).__init__()
        cdef:
            str pull_uri
            str push_uri
            str publiser_uri
        self.chunk_size = <long>CHUNKING_SIZE
        #self.chunk_buffer = []
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
        t = time.perf_counter()
        #print('R send1', self.envelope.header, len(self.envelope.data))
        self.send_socket.send_multipart(self.envelope.seal())
        #print('R send2 {0:.8f}'.format(time.perf_counter() - t))

    cdef void publish(self):
        self.publisher.send_multipart(self.envelope.seal())

    cdef list recv_loop(self):
        return self.recv_socket.recv_multipart()

    cdef void load_envelope(self, list r):
        self.envelope.load(r)

    cdef void create_state(self, string header, long length):
        if self.state.find(header) != self.state.end():
            self.state[header] += 1
        else:
            self.state[header] = 1
            #if length % self.chunk_size != 0:
            #    self.state[header] += 1

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
        #t = time.perf_counter()
        cdef long count
        cdef long i
        cdef long length
        count = self.retrieve_state(self.envelope.get_header())
        #print('Assembly', self.envelope.header)
        if self.success:
            #print(self.envelope.header)
            #self.assembly_buffer.extend(self.envelope.data)
            self.chunk_holder = self.envelope.get_data()
            #print('R a1', self.assembly_buffer)
            length = <long>len(self.chunk_holder)
            #print('R c', self.chunk_holder[0])
            #print('Rc2', self.assembly_buffer[self.envelope.get_header()])
            #print('Rc2', self.assembly_buffer[self.envelope.get_header()][0])
            #print('R i', self.index_tracker[self.envelope.get_header()], 1)
            #print(self.envelope.header)
            for i in range(length):
                #print('combined index', self.index_tracker[self.envelope.get_header()] + i, length)
                self.assembly_buffer[self.envelope.get_header()][self.index_tracker[self.envelope.get_header()] + i] = self.chunk_holder[i]
            self.index_tracker[self.envelope.get_header()] += length
            #print('R a2', self.assembly_buffer)
            #print('R it', self.index_tracker)
            #np.concatenate(
            #    (self.assembly_buffer[self.envelope.get_header()], np.frombuffer(self.envelope.data)), 
            #    axis=0
            #)
            if count == 0:
                self.envelope.set_data(self.assembly_buffer[self.envelope.get_header()])
                self.publish()
                del self.index_tracker[self.envelope.get_header()]
                del self.assembly_buffer[self.envelope.get_header()]
            #print('R assembler {0:.8f}'.format(time.perf_counter() - t))
        else:
            self.publish()
            #print('AR assembler {0:.8f}'.format(time.perf_counter() - t))
        return 0

    cdef long chunk(self) except -1:
        #cdef double t = time.perf_counter()
        cdef long i
        cdef long groups = math.ceil(self.envelope.get_length() / float(self.chunk_size))
        if self.envelope.get_length() <= 1 or self.envelope.get_length() == self.chunk_size:
            self.send()
        else:
            #print('CC', [self.envelope.get_data()])
            self.chunk_buffer = np.array_split(self.envelope.get_data(), groups, axis=0)
            self.assembly_buffer[self.envelope.get_header()] = np.empty((len(self.chunk_buffer[0]) * groups, len(self.chunk_buffer[0][0])))
            #print('assembly buff', self.assembly_buffer)
            self.index_tracker[self.envelope.get_header()] = 0
            for i in range(groups):
                #if len(self.chunk_buffer) >= self.chunk_size:
                #    self.envelope.data = self.chunk_buffer[:self.chunk_size]
                #    del self.chunk_buffer[:self.chunk_size]
                #else:
                #    self.envelope.data = self.chunk_buffer
                #    self.chunk_buffer = []
                self.envelope.set_data(self.chunk_buffer[i])
                self.create_state(self.envelope.get_header(), self.envelope.get_length())
                #print('Chunker', self.envelope.header)
                self.send()
                #print('AR chunk {0:.8f}'.format(time.perf_counter() - t))
                #t = time.perf_counter()
        return 0

    cpdef void start(self):
        cdef vector[string] raw_message
        cdef long r
        while True:
            #t = time.perf_counter()
            raw_message = self.recv_loop()
            #print('R recv_loop {0:.8f}'.format(time.perf_counter() - t))
            #t = time.perf_counter()
            self.load_envelope(raw_message)
            #print('R', self.envelope.header)
            #print('R', np.frombuffer(self.envelope.data))
            if self.envelope.get_lifespan() > 0:
                r = self.chunk()
                if r == -1:
                    raise
            else:
                r = self.assemble()
                if r == -1:
                    raise
            #print('R start', time.perf_counter() - t)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
