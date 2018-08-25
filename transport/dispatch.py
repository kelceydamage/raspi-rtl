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
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
from .conf.configuration import RELAY_ADDR
from .conf.configuration import RELAY_RECV
from .conf.configuration import RELAY_PUBLISHER
from .conf.configuration import CACHE_ADDR
from .conf.configuration import CACHE_RECV
from .conf.configuration import LOG_LEVEL
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
        super(Dispatcher, self).__init__()
        context = zmq.Context()
        self.push_socket = context.socket(zmq.PUSH)
        self.push_socket.connect('tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_RECV))
        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.connect('tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_PUBLISHER))
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
        try:
            self.req_addr = 'tcp://{}:{}'.format(CACHE_ADDR, CACHE_RECV)
            self.req_socket = zmq.Context().socket(zmq.REQ)
            self.req_socket.connect(self.req_addr)
        except Exception as e:
            printc('[CACHE_CLIENT]: (__init__) {0}'.format(str(e)), COLOURS.RED)

    def send(self, message):
        msg = [Tools.serialize(x) for x in message]
        try:
            self.req_socket.send_multipart(msg)
        except Exception as e:
            printc('[CACHE_CLIENT]: (send) {0}'.format(str(e)), COLOURS.RED)
        while True:
            try:
                r = self.req_socket.recv_multipart()
            except Exception as e:
                print(str(e))
            break
        return Tools.deserialize(r[0])

# Functions
# ------------------------------------------------------------------------ 79->
    
# Main
# ------------------------------------------------------------------------ 79->
