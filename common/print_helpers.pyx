#!python
#cython: language_level=3, cdivision=True
###boundscheck=False, wraparound=False //(Disabled by default)
# ------------------------------------------------------------------------ 79->
# Author: Kelcey Damage
# Cython: 0.28+
# Doc
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

cimport cython
from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.string cimport string
from libcpp.map cimport map as cmap
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast8_t
from libc.stdint cimport int_fast16_t
from libc.stdio cimport printf
from libc.stdio cimport sprintf
from libc.stdio cimport FILE, fopen, fwrite, fprintf, fclose
from libc.stdlib cimport atoi
from posix cimport time as p_time

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->

cdef class Logger(object):
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

    cdef object colours
    cdef unsigned int log_level
    cdef string location

    def __init__(self, unsigned int log_level):
        self.colours = Colours()
        self.log_level = log_level
        self.location = b'var/log/'

    cdef void log(self, string message, unsigned int mode=0):
        if mode < self.log_level:
            printf('%s\n', message.c_str())

    cdef int_fast16_t write(self, string line, string log) except -1:
        cdef string fname = string(self.location).append(log)
        cdef char* _file = <char *>fname.c_str()
        cdef FILE *ptr_fw
        cdef FILE *ptr_fr
        ptr_fw = fopen(_file, "ab+")
        if ptr_fw == NULL:
            return -1
        fprintf(ptr_fw, "%s\n", line.c_str())
        fclose(ptr_fw)
        return 0

    def _sprint(self, header, name, message, nline=False):
        _char = ''
        if nline:
            _char = '\n'
        return '{3}{0} {1} {2}'.format(
            padding('[{0}]:'.format(header), 16),
            padding('({0})'.format(name), 24),
            message,
            _char
            )

    cdef int_fast16_t _logw(self, dict mdict, int_fast16_t mode, string file) except? -1:
        cdef string msg = str(mdict).encode()
        cdef long err
        if mode < self.log_level:
            err = self.write(msg, file)
            if err == -1:
                return err
        return 0

    cpdef int_fast16_t logw(self, dict mdict, int_fast16_t mode=0, str file='machine.log'):
        cdef int_fast16_t r = -1
        try:
            r = self._logw(mdict, mode, file.encode())
        except Exception as e:
            print('ERR-1', e)
        return r

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

cpdef padding(message, width):
    """
    NAME:           padding

    DESCRIPTION:    Pad a string ot a certain length.
    """
    if len(message) < width:
        message += ' ' * (width - len(message))
    return message


cpdef printc(message, colour):
    """
    NAME:           printc

    DESCRIPTION:    Print a line of text in a given colour.
    """
    endc = '\033[m'
    print('{0}{1}{2}'.format(colour, message, endc))


cpdef print_stage(id, tasks):
    cdef:
        long length = len(tasks)
        object C = Colours()

    print('-' * 79)
    printc('Running Stage: [{0}]'.format(id), C.PURPLE)
    for i in range(length):
        printc('* {0}'.format(tasks[i]), C.LIGHTBLUE)

# Main
# ------------------------------------------------------------------------ 79->
