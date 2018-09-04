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
from common.datatypes import *
from common.print_helpers import Logger
import zmq

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)

# Classes
# ------------------------------------------------------------------------ 79->


class Dispatcher(object):
    """
    NAME:           Dispatcher

    DESCRIPTION:    Dispatches tasks to the relay.

    METHODS:        .send(envelope)
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
        self.sub_socket.set(zmq.SUBSCRIBE, b'0')
        self.results = []

    def _recieve(self):
        envelope = Envelope()
        envelope.load(self.sub_socket.recv_multipart())
        LOG.logc('DISPATCHER', 'receive', '<---- published', 1, 'GREEN')
        return envelope

    def close(self):
        self.push_socket.disconnect(self.push_addr)
        self.sub_socket.disconnect(self.sub_addr)

    def send(self, envelope):
        sealed = envelope.seal()
        self.sub_socket.set(zmq.SUBSCRIBE, sealed[0])
        self.push_socket.send_multipart(sealed)
        return self._recieve()


class Cache(object):
    """
    NAME:           Cache

    DESCRIPTION:    Sends cache requests to a cache node.

    METHODS:        .send(envelope)
                    Send a type Envelope() object to the cache node. This
                    is a blocking method, and will wait until the results of
                    the lookup are returned.
    """

    def __init__(self):
        context = zmq.Context()
        try:
            req_uri = 'tcp://{0}:{1}'.format(CACHE_ADDR, CACHE_RECV)
            self.req_socket = context.socket(zmq.REQ)
            self.req_socket.connect(req_uri)
            self.pipeline = Pipeline()
            self.pipeline.tasks = ['cache']
            self.meta = Meta()
        except Exception as e:
            LOG.loge('CACHE_CLIENT', '__init__', e)

    def send(self, method, key=None, value=None):
        envelope = Envelope()
        envelope.pack(
            method,
            self.meta.extract(),
            self.pipeline.extract(),
            (key, value)
            )
        try:
            self.req_socket.send_multipart(envelope.seal())
        except Exception as e:
            LOG.loge('CACHE', 'send', e)
        try:
            envelope.load(self.req_socket.recv_multipart())
        except Exception as e:
            LOG.loge('CACHE', 'recv', e)
        header, meta, pipeline, data = envelope.unpack()
        return data

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
