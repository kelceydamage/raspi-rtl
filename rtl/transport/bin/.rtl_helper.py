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
import sys
import argparse
import time
from multiprocessing import Process
os.sys.path.append('{0}{1}'.format(os.getcwd().split('rtl')[0], 'rtl'))
from rtl.transport.registry import load_tasks
from rtl.transport.node import TaskNode, CacheNode, PlotNode
from rtl.transport.relay import Relay
from rtl.transport.conf.configuration import *
from rtl.common.print_helpers import Logger, Colours

# Globals
# ------------------------------------------------------------------------ 79->
RUNDIR = os.path.expanduser(PIDFILES)
COLOURS = Colours()
LOG_LEVEL = 1
LOG = Logger(LOG_LEVEL)
NODES = {
    0: Relay,
    1: TaskNode,
    2: CacheNode,
    3: PlotNode
}

# Parser
# ------------------------------------------------------------------------ 79->
parser = argparse.ArgumentParser(prog="Task Engine")
group_2 = parser.add_argument_group('Mode Of Operation')
group_2.add_argument(
    '-r',
    "--relay",
    dest="relay",
    help="Specify number of relays to start"
    )
group_2.add_argument(
    '-t',
    "--task",
    dest="task",
    help="Specify number of tasknodes to start"
    )
group_2.add_argument(
    '-c',
    "--cache",
    dest="cache",
    help="Specify number of cachenodes to start"
    )
group_2.add_argument(
    '-p',
    "--plot",
    dest="plot",
    help="Specify number of plotnodes to start"
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


def start_node(_type, count, functions=''):
    for i in range(int(count)):
        service = NODES[_type]
        start(service, functions)


def service_wrapper(service, functions):
    service(functions).start()


def start(service, functions):
    p = Process(target=service_wrapper, args=[service, functions])
    p.daemon = True
    p.start()


def validate(param):
    if param is not None:
        if int(param) > 0:
            return True
        return False
    return True


def select_value(arg=None, conf=0):
    if arg is not None:
        return arg
    if conf > 0:
        return conf
    return 0


def launcher(args, functions):
    success = False
    if validate(args.relay):
        try:
            start_node(0, select_value(args.relay, 1))
            if DEBUG: print('Launching RELAY')
            success = True
        except Exception as e:
            print(e)
    if validate(args.task):
        try:
            start_node(1, select_value(args.task, TASK_WORKERS), functions)
            if DEBUG: print('Launching TASK')
            success = True
        except Exception as e:
            print(e)
    if validate(args.cache):
        try:
            start_node(2, select_value(args.cache, CACHE_WORKERS))
            if DEBUG: print('Launching CACHE')
            success = True
        except Exception as e:
            print(e)
    if validate(args.plot):
        try:
            start_node(3, select_value(args.plot, PLOT_WORKERS))
            if DEBUG: print('Launching PLOT')
            success = True
        except Exception as e:
            print(e)
    return success


# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    pid = os.getpid()
    try:
        path = [x for x in sys.path if "site-packages" in x][0]
        functions = load_tasks('{0}/{1}'.format(path, 'rtl/tasks'))
    except Exception as e:
        print(str(e))
        quit()
    args = args[0]
    if args.meta:
        print_meta(functions)
        exit(1)
    if not launcher(args, functions):
        print(parser.print_help())
        exit(1)
    print('Starting RTL')
    with open('{0}{1}-{2}'.format(RUNDIR,'master', pid), 'w+') as f:
        f.write(str(pid))
    while True:
        time.sleep(1000)