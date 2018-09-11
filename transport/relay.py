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
from transport.conf.configuration import CHUNKING
from transport.conf.configuration import CHUNKING_SIZE
from transport.conf.configuration import LOG_LEVEL
from transport.conf.configuration import RELAY_LISTEN
from transport.conf.configuration import RELAY_RECV
from transport.conf.configuration import RELAY_SEND
from transport.conf.configuration import RELAY_PUBLISHER
from transport.conf.configuration import CACHED
from transport.conf.configuration import PROFILE
from transport.cache import Cache
from common.datatypes import *
from common.encoding import Tools
from common.print_helpers import Logger
from common.print_helpers import timer
import zmq
import os

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)
VERSION = '0.4'
CHUNKING = True
CACHE = Cache()

# Classes
# ------------------------------------------------------------------------ 79->


class Relay(object):
    """
    NAME:           Router

    DESCRIPTION:    Routes messages to available workers.

    METHODS:        .log_wrapper(msg, mode=0, colour='GREEN')
                    Wrapper for logger to clean up code.

                    .ship(header, meta, pipeline)
                    Send the envelope to a node.

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

                    .empty_cache()
                    Delete task cache entries in cache.

                    .start()
                    Start the relay and begin listening.
    """

    @timer(LOG, 'relay', PROFILE)
    def __init__(self, functions=''):
        super(Relay, self).__init__()
        self.pid = os.getpid()
        self.log_msg = {
            'system': 'relay-{0}'.format(self.pid),
            'name': self.__init__.__name__,
            }
        with open('var/run/{0}'.format(self.log_msg['system']), 'w+') as f:
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
        self.state = {}
        self.buffer = []
        self.queue = []
        self.cache_keys = []
        self.envelope = Envelope(cached=CACHED)
        self.log_wrapper('online', mode=0)

    def log_wrapper(self, msg, mode=0, colour='GREEN'):
        self.log_msg['message'] = msg
        self.log_msg['colour'] = colour
        LOG.logw(self.log_msg, mode, 'machine.log')

    @timer(LOG, 'relay', PROFILE)
    def send(self):
        self.log_msg['name'] = self.send.__name__
        self.send_socket.send_multipart(self.envelope.seal())
        self.buffer = []
        self.log_wrapper('sent ---->', mode=2, colour='PURPLE')

    def publish(self):
        self.publisher.send_multipart(self.envelope.seal())

    @timer(LOG, 'relay', PROFILE)
    def recv_loop(self):
        return self.recv_socket.recv_multipart()

    @timer(LOG, 'relay', PROFILE)
    def load_envelope(self, r):
        self.envelope.load(r)

    @timer(LOG, 'relay', PROFILE)
    def create_state(self, header, length):
        self.log_msg['name'] = self.create_state.__name__
        self.log_wrapper(self.state, mode=3, colour='PURPLE')
        if header not in self.state.keys():
            self.state[header] = 1
            if length % CHUNKING_SIZE != 0:
                self.state[header] += 1
        else:
            self.state[header] += 1

    @timer(LOG, 'relay', PROFILE)
    def retrieve_state(self, header):
        self.log_msg['name'] = self.retrieve_state.__name__
        self.log_wrapper(self.state, mode=3, colour='PURPLE')
        if header in self.state.keys():
            self.state[header] -= 1
            if self.state[header] == 0:
                self.state.pop(header, None)
                return True, 0
            return True, self.state[header]
        return False, 0

    @timer(LOG, 'relay', PROFILE)
    def assemble(self):
        self.log_msg['name'] = self.assemble.__name__
        self.envelope.cached = False
        header = self.envelope.get_header()
        success, count = self.retrieve_state(header)
        if success:
            self.queue.extend(self.envelope.get_data())
            if count == 0:
                self.envelope.data = self.queue
                self.empty_cache()
                self.publish()
                self.queue = []
                self.log_wrapper('published ---->', mode=2, colour='PURPLE')
        else:
            self.empty_cache()
            self.publish()
            print('send to client single')
            self.log_wrapper('published ---->', mode=2, colour='PURPLE')

    @timer(LOG, 'relay', PROFILE)
    def chunk(self):
        length = self.envelope.length
        if length <= 1 or length == CHUNKING_SIZE:
            self.send()
        else:
            self.envelope.compressed = False
            data = self.envelope.data
            self.envelope.data = []
            while data:
                self.buffer.append(data.pop())
                if len(self.buffer) % CHUNKING_SIZE == 0:
                    self.create_state(self.envelope.header, length)
                    self.envelope.data = self.buffer
                    self.send()
            if len(self.buffer) > 0:
                self.envelope.data = self.buffer
                self.send()

    @timer(LOG, 'relay', PROFILE)
    def empty_cache(self):
        while self.cache_keys:
            r = CACHE.delete(self.cache_keys.pop())
            if not r[1]:
                raise
        CACHE.sync()

    @timer(LOG, 'relay', PROFILE)
    def start(self):
        self.log_msg['name'] = self.start.__name__
        while True:
            r = self.recv_loop()
            self.load_envelope(r)
            # -----------------------
            # Caching stuff
            # -----------------------
            # if envelope.manifest['meta']['spent_key'] is not None:
            #    self.cache_keys.append(envelope.manifest['meta']['spent_key'])
            #    envelope.manifest['meta']['spent_key'] = None
            # if len(self.cache_keys) >= 100:
            #    self.empty_cache()
            self.log_wrapper('<---- recieved', mode=2, colour='PURPLE')
            self.log_wrapper(self.envelope.get_meta(), mode=4, colour='BLUE')
            if self.envelope.lifespan > 0:
                self.chunk()
            else:
                self.assemble()

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
