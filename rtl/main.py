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
#   rtl.transport
#   rtl.common
#   multiprocessing
#   argparse
#   time
#   os
#
# Imports
# ------------------------------------------------------------------------ 79->
import os
import argparse
import time
from multiprocessing import Process
from rtl.transport.registry import importTasks
from rtl.transport.node import TaskNode
from rtl.transport.node import CacheNode
from rtl.transport.node import PlotNode
from rtl.transport.relay import Relay
from rtl.transport.conf.configuration import *
from rtl.common.print_helpers import Colours


# Globals
# ------------------------------------------------------------------------ 79->
RUNDIR = os.path.expanduser(PIDFILES)
COLOURS = Colours()
NODES = {
    'relay': Relay,
    'task': TaskNode,
    'plot': PlotNode,
    'cache': CacheNode
}
COUNTS = {
    'relay': 1,
    'task': TASK_WORKERS,
    'plot': PLOT_WORKERS,
    'cache': CACHE_WORKERS
}


# Parser
# ------------------------------------------------------------------------ 79->
parser = argparse.ArgumentParser(prog="Task Engine")
group = parser.add_argument_group('Extras')
group.add_argument(
    '-m',
    "--meta",
    action="store_true",
    default=False,
    help="Print meta header"
    )
args = parser.parse_known_args()


# Classes
# ------------------------------------------------------------------------ 79->
class StartError(Exception):
    """Micro-service failed to start"""

    def __init__(self, error):
        self.error = error


# Functions
# ------------------------------------------------------------------------ 79->
def printMeta(functions):
    """Print the loaded tasks to the console.

    Args:
        functions (dict): The dict of task modules the platform has loaded 
            into memory and stored as a reference.

    """
    print('-' * 79)
    print('REGISTERED-TASKS:')
    print('-' * 79)
    for key in functions.keys():
        print(' {0}{1}__{2} {3}{4}{2}'.format(
            COLOURS.BCYAN,
            COLOURS.BLACK,
            COLOURS.ENDC,
            COLOURS.LIGHTBLUE,
            key
            ))
    print('-' * 79)

def launcher():
    """Main loop for lanching services.

    Returns:
        bool: True if all micro-services launched successfully, False otherwise.
    
    """
    for service in COUNTS:
        success = launch(service)
    return success

def launch(service):
    """Call startNode on each service and check for exceptions.

    Args:
        service (str): The short name for the micro-service to be started.

    Returns:
        bool: True if all micro-services launched successfully, False otherwise.
    
    """
    if DEBUG: print('Launching', service.upper())
    try:
        startNode(service)
    except StartError:
        return False
    return True

def startNode(service):
    """Start a subprocess for each micro-service

    Args:
        service (str): The short name for the micro-service to be started.

    """
    for i in range(COUNTS[service]):
        p = Process(
            target=serviceWrapper,
            args=[NODES[service]]
        )
        p.daemon = True
        p.start()

def serviceWrapper(serviceClass):
    """Call start on the the service inside the process.

    Args:
        serviceClass (class): The reference to the class to be started in this 
            subprocess.

    Raise:
        StartError: if service failes to start.

    """
    try:
        serviceClass().start()
    except Exception as e:
        raise StartError(e)


# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    pid = os.getpid()
    functions = importTasks(TASK_LIB)
    if args[0].meta:
        printMeta(functions)
        exit(1)
    if not launcher():
        print('Failed to launch one or more micro-services')
        exit(1)
    print('Starting RTL')
    with open('{0}{1}-{2}'.format(RUNDIR,'master', pid), 'w+') as f:
        f.write(str(pid))
    while True:
        time.sleep(1000)
