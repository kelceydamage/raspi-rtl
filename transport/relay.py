#!/usr/bin/env python3
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
#                   conf
#                   common
#                   zmq
#    
# Imports
# ------------------------------------------------------------------------ 79->
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from conf.configuration import CHUNKING
from conf.configuration import CHUNKING_SIZE
from conf.configuration import LOG_LEVEL
from common.datatypes import *
from common.print_helpers import Logger
import zmq

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)
VERSION                 = b'0.1'
CHUNKING = True
CHUNKING_SIZE = 2

# Classes
# ------------------------------------------------------------------------ 79->
class Relay(object):
    """
    NAME:           Router

    DESCRIPTION:    Routes messages to available workers.

    METHODS:        .ship(header, meta, pipeline)
                    Pack the envelope and send to a node.

                    .receive()
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
    def __init__(self, host, recv_port, send_port, publisher_port, pid):
        super(Relay, self).__init__()
        context = zmq.Context()
        self.recv_socket = context.socket(zmq.PULL) # ROUTER
        self.send_socket = context.socket(zmq.PUSH) # DEALER
        self.publisher = context.socket(zmq.PUB)
        self.recv_socket.bind('tcp://{0}:{1}'.format(host, recv_port))
        self.send_socket.bind('tcp://{0}:{1}'.format(host, send_port))
        self.publisher.bind('tcp://{0}:{1}'.format(host, publisher_port))
        self.pid = pid
        self.state = {}
        self.buffer = []
        self.queue = []
        LOG.logc('RELAY-{0}'.format(self.pid), 'Startup', 'Online', 0, 'GREEN')

    def ship(self, header, meta, pipeline):
        envelope = Envelope()
        envelope.pack(header, meta.extract(), pipeline.extract(), self.buffer)
        self.send_socket.send_multipart(envelope.seal())
        self.buffer = []
        LOG.logc('RELAY', 'ship', 'sent ---->', 1, 'PURPLE')

    def receive(self):
        envelope = Envelope()
        envelope.load(self.recv_socket.recv_multipart())
        return envelope

    def create_state(self, meta):
        if not isinstance(meta.stage, bytes):
            stage = meta.stage.encode()
        else:
            stage = meta.stage
        if stage not in self.state.keys():
            meta.stage = Tools.create_id()
            self.state[meta.stage] = 1
            if meta.length % CHUNKING_SIZE != 0:
                self.state[meta.stage] += 1
        else:
            self.state[stage] += 1
        return meta

    def retrieve_state(self, meta):
        stage = meta.stage.encode()
        if stage in self.state.keys():
            self.state[stage] -= 1
            if self.state[stage] == 0:
                self.state.pop(stage, None)
                return meta, True, 0
            return meta, True, self.state[stage]
        return meta, False, 0

    def assemble(self, envelope):
        header, meta, pipeline, data = envelope.unpack()
        meta, success, count = self.retrieve_state(meta)
        LOG.logc('RELAY', 'state in', self.state, 2, 'PURPLE')
        if success:
            self.queue.extend(data)
            if count == 0:
                envelope.pack(header, meta.extract(), pipeline.extract(), self.queue)
                self.publisher.send_multipart(envelope.seal())
                self.queue = []
                LOG.logc('RELAY', 'assemble', 'published ---->', 1, 'PURPLE')
        else:
            self.publisher.send_multipart(envelope.seal())
            print('send to client single')
            LOG.logc('RELAY', 'assemble', 'published ---->', 1, 'PURPLE')

    def chunk(self, envelope):
        header, meta, pipeline, data = envelope.unpack()
        if envelope.length <= 1 or envelope.length == CHUNKING_SIZE:
            self.buffer = data
            self.ship(header, meta, pipeline)
        else:
            for i in range(len(data)):
                self.buffer.append(data.pop())
                if len(self.buffer) % CHUNKING_SIZE == 0:
                    meta = self.create_state(meta)
                    self.ship(header, meta, pipeline)
            if len(self.buffer) > 0:
                self.ship(header, meta, pipeline)
        del envelope
        LOG.logc('RELAY', 'state out', self.state, 2, 'PURPLE')

    def start(self):
        while True:
            envelope = self.receive()
            LOG.logc('RELAY', 'start', '<---- recieved', 1, 'PURPLE')
            LOG.logc('RELAY', 'start', envelope.open(), 3, 'BLUE')
            if envelope.lifespan > 0:
                self.chunk(envelope)
            else:
                self.assemble(envelope)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
