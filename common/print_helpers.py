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
#
# Imports
# ------------------------------------------------------------------------ 79->
import functools
import time

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->


class Logger(object):
    """
    NAME:           Logger

    DESCRIPTION:    Provides a basic logger to stdout

    METHODS:        .log(message, mode=0)
                    Basic logger prints message to screen if mode less then
                    log_mode

                    .write(line, log)
                    Write a line to a specific log file.

                    ._sprint(header, name, message, nline=False)
                    Format a log line for human readable output.

                    .logw(mdict, mode=0, file='machine.log')
                    Logwriter for writing to files. Default file is the
                    machine.log.

                    .logd(mdict, mode=0, colour='RED')
                    Logwriter for writing to stdout. Default color is red.
    """
    def __init__(self, log_level):
        self.colours = Colours()
        self.log_level = log_level
        self.location = 'var/log/'

    def log(self, message, mode=0):
        if mode < self.log_level:
            print(message)

    def write(self, line, log):
        try:
            with open('{0}{1}'.format(self.location, log), 'a+') as f:
                f.write('{0}\n'.format(line))
        except Exception as e:
            print('ERROR', e)
            raise

    def _sprint(self, header, name, message, nline=False):
        char = ''
        if nline:
            char = '\n'
        return '{3}{0} {1} {2}'.format(
            padding('[{0}]:'.format(header), 16),
            padding('({0})'.format(name), 24),
            message,
            char
            )

    def logw(self, mdict, mode=0, file='machine.log'):
        if mode < self.log_level:
            self.write(mdict, file)

    def logd(self, mdict, mode=0, colour='RED'):
        if mode < self.log_level:
            msg = self._sprint(
                mdict['system'],
                mdict['name'],
                mdict['message']
                )
            printc(msg, getattr(self.colours, colour))


class Colours(object):
    """
    NAME:           Colours

    DESCRIPTION:    Provides templated print colours for printc

    self.RED             = '\033[38;5;1m'
    self.BLUE             = '\033[38;5;12m'
    self.GREEN             = '\033[38;5;10m'
    self.CORAL             = '\033[38;5;9m'
    self.DARKBLUE        = '\033[38;5;4m'
    self.PURPLE            = '\033[38;5;5m'
    self.CYAN            = '\033[38;5;6m'
    self.LIGHTBLUE        = '\033[38;5;14m'
    self.BRED            = '\033[48;5;1m'
    self.BBLUE            = '\033[48;5;12m'
    self.BGREEN            = '\033[48;5;10m'
    self.BCORAL            = '\033[48;5;9m'
    self.BDARKBLUE        = '\033[48;5;4m'
    self.BPURPLE        = '\033[48;5;5m'
    self.BCYAN             = '\033[48;5;6m'
    self.BLIGHTBLUE        = '\033[48;5;14m'
    self.BLACK            = '\033[38;5;0m'
    self.ENDC             = '\033[m'
    """
    def __init__(self):
        super(Colours, self).__init__()
        self.RED = '\033[38;5;1m'
        self.BLUE = '\033[38;5;12m'
        self.GREEN = '\033[38;5;10m'
        self.CORAL = '\033[38;5;9m'
        self.DARKBLUE = '\033[38;5;4m'
        self.PURPLE = '\033[38;5;5m'
        self.CYAN = '\033[38;5;6m'
        self.LIGHTBLUE = '\033[38;5;14m'
        self.BRED = '\033[48;5;1m'
        self.BBLUE = '\033[48;5;12m'
        self.BGREEN = '\033[48;5;10m'
        self.BCORAL = '\033[48;5;9m'
        self.BDARKBLUE = '\033[48;5;4m'
        self.BPURPLE = '\033[48;5;5m'
        self.BCYAN = '\033[48;5;6m'
        self.BLIGHTBLUE = '\033[48;5;14m'
        self.BLACK = '\033[38;5;0m'
        self.ENDC = '\033[m'

# Functions
# ------------------------------------------------------------------------ 79->


def padding(message, width):
    """
    NAME:           padding

    DESCRIPTION:    Pad a string ot a certain length.
    """
    if len(message) < width:
        message += ' ' * (width - len(message))
    return message


def printc(message, colour):
    """
    NAME:           printc

    DESCRIPTION:    Print a line of text in a given colour.
    """
    endc = '\033[m'
    print('{0}{1}{2}'.format(colour, message, endc))


def timer(logger, system, enabled=False):
    """
    NAME:           timer

    DESCRIPTION:    Decorator for logging execution time of wrapped methods.
    """
    def timer_wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            if enabled:
                start = time.perf_counter()
            value = func(*args, **kwargs)
            if enabled:
                log_msg = {
                    'system': system,
                    'name': func.__name__,
                    'message': 'perf-wrapper',
                    'perf_time': '{:4.8f}'.format(time.perf_counter() - start)
                }
                logger.logd(log_msg, mode=1, colour='LIGHTBLUE')
                logger.logw(log_msg, mode=1, file='performance.log')
            return value
        return inner_wrapper
    return timer_wrapper

# Main
# ------------------------------------------------------------------------ 79->
