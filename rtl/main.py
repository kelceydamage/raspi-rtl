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
"""
This module provides functionality to the raspi-rtl shell script.

Note:
    This script should only be run from the main raspi-rtl shell script.

Attributes:
    COLOURS (object): class of terminal colours.
    NODES (list): A list of node objects containing a class reference and a
        count.

Todo
    * Find a better way to handle args in the ``run`` function (less \
        cyclomatic complexity).

"""


# Imports
# ------------------------------------------------------------------------ 79->
import os
import argparse
import time
from multiprocessing import Process
from rtl.transport.registry import import_tasks
from rtl.transport.node import TaskNode
from rtl.transport.node import PlotNode
from rtl.transport.relay import Relay
from rtl.transport.conf import configuration as conf
from rtl.common.print_helpers import Colours
from rtl.common.logger import log


# Const
# ------------------------------------------------------------------------ 79->
COLOURS = Colours()
NODES = [
    {
        'class': Relay,
        'count': 1
    },
    {
        'class': TaskNode,
        'count': conf.TASK_WORKERS
    },
    {
        'class': PlotNode,
        'count': conf.PLOT_WORKERS
    }
]


# Classes
# ------------------------------------------------------------------------ 79->
class StartError(Exception):
    """Micro-service failed to start"""

    def __init__(self, error):
        super(StartError, self).__init__()
        self.error = error


class Launcher(object):
    """Launcher is class for handling all the setup logic for running an RTL
    cluster.

    Attributes:
        nodes (list): A list of node objects defined in the beginning of this
            module/
        conf (module): The configuration module.
        parser (class): ArgumentParser class object.
        args (class): Namespace class object:

            - meta (bool): True to print meta, else False to run script.
            - no_server (bool): Default to False, pass True for tests.
        functions (dict): A dict of task modules.

    """
    def __init__(self):
        """Initializer for the ``Launcher`` class.

        """
        self.nodes = NODES
        self.conf = conf
        self.parser = argparse.ArgumentParser(prog="Task Engine")
        self.parser.add_argument(
            '-m',
            "--meta",
            action="store_true",
            default=False,
            help="Print meta header"
            )
        self.parser.add_argument(
            '-n',
            "--no-server",
            action="store_true",
            default=False,
            help="do not start server loop"
            )
        self.args = self.parser.parse_known_args()[0]
        self.functions = import_tasks(self.conf.TASK_LIB)
        self._store_pid()

    def _print_meta(self):
        """Print the loaded tasks to the console.

        Warning:
            This is a private member and should never be called directly.

        Raises:
            SystemExit: natural termination point for program.

        """
        print('-' * 79)
        print('REGISTERED-TASKS:')
        print('-' * 79)
        for key in self.functions.keys():
            print(' {0}{1}__{2} {3}{4}{2}'.format(
                COLOURS.BCYAN,
                COLOURS.BLACK,
                COLOURS.ENDC,
                COLOURS.LIGHTBLUE,
                key
                ))
        print('-' * 79)
        raise SystemExit

    def _launch(self, service_class, count):
        """Call startNode on each service and check for exceptions.

        Warning:
            This is a private member and should never be called directly.

        Args:
            service_class (ClassType): The name of a valude service class.
            count (int): the number of service_class instances to start.

        Returns:
            bool: True if all services launched successfully, False otherwise.

        """
        try:
            self._start_node(service_class, count)
        except StartError:
            return False
        return True

    def _start_node(self, service_class, count):
        """Start a subprocess for each micro-service

        Warning:
            This is a private member and should never be called directly.

        Args:
            service_class (ClassType): The name of a valude service class.
            count (int): the number of service_class instances to start.

        """
        if count == 0:
            raise StartError('Invalid count, can not launch 0 services')
        for _ in range(count):
            process = Process(
                target=_service_wrapper,
                args=[service_class]
            )
            process.daemon = True
            process.start()

    def _store_pid(self):
        """store_pid function for storing the scripts pid

        Warning:
            This is a private member and should never be called directly.

        Note
            This method writes a pidfile to ``self.conf.PIDFILES`` containing
            the pid value.

        """
        pid = os.getpid()
        rundir = os.path.expanduser(self.conf.PIDFILES)
        with open('{0}{1}-{2}'.format(rundir, 'master', pid), 'w+') as file:
            file.write(str(pid))

    def _keep_alive(self):
        """serve function for executing the main process loop

        Warning:
            This is a private member and should never be called directly.

        Raises:
            SystemExit: natural termination point for program if testing flag
                ``no_server`` is True.

        """
        if self.args.no_server:
            raise SystemExit('Exited for code testing')
        while True:
            time.sleep(1000)

    def run(self):
        """Main loop for lanching services. This is the main entry point for
        running the CLI.

        Hint:
            This is the main entry point and how you should interact with this
            class

        Example:
            .. code-block:: Python

                Launcher().run()

        Raises:
            SystemExit: if any services fail to start.

        """
        if self.args.meta:
            self._print_meta()
        for service in self.nodes:
            log('Launching {0}'.format(service['class']))
            success = self._launch(
                service['class'],
                service['count']
            )
        if not success:
            raise SystemExit('Failed to launch one or more micro-services')
        self._keep_alive()


# Functions
# ------------------------------------------------------------------------ 79->
def _service_wrapper(service_class):
    """Call start on the the service inside the process.

    Warning:
        This is a private member and should never be called directly.

    Args:
        service_class (ClassType): The name of a valude service class.

    Raise:
        StartError: if service failes to start.

    """
    try:
        service_class().start()
    except Exception as error:
        raise StartError(error)


# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':  # pragma: no cover
    # Call the Launcher class and invoke the run method.
    Launcher().run()
