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
from transport.conf.configuration import CACHE_MAP_SIZE
from transport.conf.configuration import CACHE_PATH
from transport.conf.configuration import PROFILE
from common.datatypes import *
from common.print_helpers import Logger
from common.print_helpers import timer
import zmq
import lmdb
import time

# Globals
# ------------------------------------------------------------------------ 79->
LOG = Logger(LOG_LEVEL)
VERSION = '0.4'

# Classes
# ------------------------------------------------------------------------ 79->


class Dispatcher(object):
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

    @timer(LOG, 'dispatcher', PROFILE)
    def __init__(self):
        self.log_msg = {
            'system': 'dispatcher',
            'name': self.__init__.__name__,
            }
        context = zmq.Context()
        push_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_RECV)
        pull_uri = 'tcp://{0}:{1}'.format(RELAY_ADDR, RELAY_PUBLISHER)
        self.push_socket = context.socket(zmq.PUSH)
        self.sub_socket = context.socket(zmq.SUB)
        self.push_socket.connect(push_uri)
        self.log_wrapper('connected-relay', mode=4)
        self.sub_socket.connect(pull_uri)
        self.log_wrapper('connected-publisher', mode=4)
        self.results = []

    def log_wrapper(self, msg, mode=0, colour='GREEN'):
        self.log_msg['message'] = msg
        self.log_msg['colour'] = colour
        LOG.logw(self.log_msg, mode, 'machine.log')

    @timer(LOG, 'dispatcher', PROFILE)
    def _recieve(self):
        self.log_msg['name'] = self._recieve.__name__
        envelope = Envelope()
        envelope.load(self.sub_socket.recv_multipart())
        self.log_wrapper('<---- published', mode=1)
        return envelope

    @timer(LOG, 'dispatcher', PROFILE)
    def close(self):
        self.log_msg['name'] = self.close.__name__
        self.push_socket.disconnect(self.push_addr)
        self.sub_socket.disconnect(self.sub_addr)
        self.log_wrapper('connection-closed', mode=4)

    @timer(LOG, 'dispatcher', PROFILE)
    def send(self, envelope):
        self.log_msg['name'] = self.send.__name__
        self.log_wrapper('starting job', mode=0)
        sealed = envelope.seal()
        self.sub_socket.set(zmq.SUBSCRIBE, sealed[0])
        self.log_wrapper('subscribed-{0}'.format(sealed[0]), mode=4)
        self.push_socket.send_multipart(sealed)
        self.log_wrapper('dispatch-sent', mode=3)
        return self._recieve()


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
