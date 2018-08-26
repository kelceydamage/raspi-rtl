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
#                   transport
#                   common
#                   argparse
#                   time
#
# Imports
# ------------------------------------------------------------------------ 79->
import os
os.sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
                )
            )
        )
    )
from transport.registry import load_tasks
from transport.node import TaskNode, CacheNode
from transport.relay import Relay
from transport.conf.configuration import *
from common.spawner import ProcessHandler
from common.print_helpers import Logger, Colours
import argparse
import time

# Globals
# ------------------------------------------------------------------------ 79->
COLOURS = Colours()
LOG_LEVEL = 1
LOG = Logger(LOG_LEVEL)

# Parser
# ------------------------------------------------------------------------ 79->
parser = argparse.ArgumentParser(prog="Task Engine")
group_1 = parser.add_argument_group('Mode Of Operation')
group_1.add_argument(
    'mode', 
    nargs='?',
    help='Available modes: ROUTER, TASK, CACHE'
    )
group_2 = parser.add_argument_group('Parameters')
group_2.add_argument(
    '-a', 
    "--address", 
    dest="address", 
    help="Specify listening ip address [ex: 0.0.0.0]"
    )
group_2.add_argument(
    '-p', 
    "--port", 
    dest="port", 
    help="Specify listening port [ex: 10001]"
    )
group_3 = parser.add_argument_group('Extras')
group_3.add_argument(
    '-m', 
    "--meta",
    action="store_true",
    default=False,
    help="Print meta header"
    )
args = parser.parse_known_args()

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def start_worker(args, pid):
    if args[-1] == 0:
        try:
            LOG.logn('START', 'Relay-{0}'.format(pid), 'Starting', 0, 'LIGHTBLUE')
            Relay(
                host=RELAY_LISTEN,
                recv_port=RELAY_RECV,
                send_port=RELAY_SEND,
                publisher_port=RELAY_PUBLISHER,
                pid=pid
                ).start()
        except Exception as e:
            LOG.loge('START', 'start_worker', 'Relay {0}'.format(e))
    elif args[-1] == 1:
        time.sleep(0.5)
        try:
            LOG.logc('START', 'TaskNode-{0}'.format(pid), 'Starting', 0, 'LIGHTBLUE')
            TaskNode(
                relay=RELAY_ADDR, 
                recv_port=RELAY_SEND,
                send_port=RELAY_RECV,
                pid=pid,
                functions=args[2],
                ).start()
        except Exception as e:
            LOG.loge('START', 'start_worker', 'TaskNode {0}'.format(e))
    elif args[-1] == 2:
        time.sleep(0.5)
        try:
            LOG.logc('START', 'CacheNode-{0}'.format(pid), 'Starting', 0, 'LIGHTBLUE')
            CacheNode(
                host=CACHE_LISTEN,
                port=CACHE_RECV,
                pid=pid
                ).start()
        except Exception as e:
            LOG.loge('START', 'start_worker', 'CacheNode {0}'.format(e))

def gen_services(host, port, mode, functions):

    def _loop(count, worker_type, port, host, functions=''):
        for i in range(count):
            SERVICES.append([start_worker, [host, port, functions, worker_type]])
        return SERVICES

    SERVICES = []
    try:
        if mode == 'router':
            if host == None:
                raise
            else:
                SERVICES = _loop(1, 0, port, host)
        elif mode == 'task':
            if host == None or port == None:
                raise
            else:
                SERVICES = _loop(TASK_WORKERS, 1, port, host, functions)
        elif mode == 'cache':
            if host == None:
                raise
            else:
                SERVICES = _loop(CACHE_WORKERS, 2, port, host)
    except Exception as e:
        msg = 'Invald options and arguments provided. Unable to start services'
        LOG.loge('START', 'gen_services', msg)
        exit(1)
    return SERVICES, functions

def print_meta(functions):
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

# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    try:
        functions = load_tasks('tasks')
    except Exception as e:
        print(str(e))
        quit()
    args = args[0]
    if not args.mode or not args.address:
        if args.meta:
            print_meta(functions)
            exit(0)
        parser.print_help()
        exit(1)
    if args.meta:
        print_meta(functions)
    SERVICES, functions = gen_services(
        args.address, 
        args.port, 
        args.mode.lower(), 
        functions
        )
    PH = ProcessHandler(SERVICES)
    PH.start(False)
