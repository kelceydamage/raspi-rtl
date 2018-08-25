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
# dependancies:
#                   multiprocessing
#                   print_helpers
#                   os
#                   signal
#                   sys
#
# Imports
# ------------------------------------------------------------------------ 79->
from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import Queue
from multiprocessing import current_process
from common.print_helpers import Logger
import os
import signal
import sys

# Globals
# ------------------------------------------------------------------------ 79->
LOG_LEVEL = 0
LOG = Logger(LOG_LEVEL)

# Classes
# ------------------------------------------------------------------------ 79->
class ProcessSpawner(object):
    """
    NAME:           ProcessSpawner

    DESCRIPTION:    A class for spawning child services and collapsing them.

    METHODS:        .spawn(services)
                    Start the spawner main process.

                    ._child_process(services)
                    Start the actual processes scheduled to be started.

                    .kill_proc(status)
                    Kill processes that where started by the spawner.
    """
    def __init__(self):
        super(ProcessSpawner, self).__init__()
        self.status = []

    def spawn(self, services):
        current_process().daemon = False
        self.q = Queue()
        p = Process(
            target=self._child_process,
            args=[services]
            )
        p.start()
        status = [] 
        for service in services:
            queue_response = self.q.get(timeout=4)
            self.status.append(queue_response)

    def _child_process(self, services):

        def __start(self, service):
            try:
                pid = os.getpid()
                reply = ['success', pid, service] 
                self.q.put(reply)
                service[0](service[1], pid)
            except Exception as e:
                LOG.loge('SPAWNER','__start', e)
                reply = ['FAIL: {0}'.format(e), pid, service] 
                self.q.put(reply)

        for service in services:
            p = Process(
                target=__start,
                args=[self, service]
                )
            p.start()

    def kill_proc(self, status):
        for process in status:
            try:
                os.kill(int(process[1]), signal.SIGTERM)
            except OSError as e:
                LOG.loge('SPAWNER','kill_proc', e)
            else:
                msg = 'Sucessfully terminated process {0[1]}: {0[2][0]}'.format(process)
                LOG.logc('SPAWNER','kill_proc', msg, 0, 'GREEN')

class ProcessHandler(ProcessSpawner):
    """
    NAME:           ProcessHandler

    DESCRIPTION:    Handles the safe exit and cleanup of spawning multiple 
                    processes.

    METHODS:        .start(standalone=True)
                    Handler for spawning services.

                    .ctrl_c(signal, frame)
                    Kills spawned services.
    """
    def __init__(self, services):
        super(ProcessHandler, self).__init__()
        self.services = services
        signal.signal(signal.SIGINT, self.ctrl_c)

    def start(self, standalone=True):
        if standalone:
            msg = 'Type [ctrl-c] to exit and shutdown workers'
            LOG.logn('HANDLER', 'start', msg, 0, 'PURPLE')
        else:
            msg = 'Starting cluster of {0} service type: {1}'.format(
                len(self.services),
                self.services[0][1][-1]
            )
            LOG.logn('HANDLER', 'start', msg, 0, 'PURPLE')
        self.spawn(self.services)

    def ctrl_c(self, signal, frame):
        msg = 'Closing application and stopping services'
        LOG.logn('HANDLER', 'ctrl_c', msg, 0, 'PURPLE')
        self.kill_proc(self.status)
        sys.exit(0)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
