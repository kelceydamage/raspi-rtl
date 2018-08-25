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

                    .logm(message, mode=0, colour='RED')
                    Logger that allows the header, name, and message to be
                    passed as a list

                    .logc(header, name, message, mode=0, colour='RED)
                    Logger that allows specifying the colour.

                    .logn(header, name, message, mode=0, colour='RED')
                    logc but with a newline at the front.

                    .loge(header, name, message, mode=0)
                    Error logger prints in red.
    """
    def __init__(self, log_level):
        self.colours = Colours()
        self.log_level = log_level

    def log(self, message, mode=0):
        if mode < self.log_level:
            print(message)

    def _sprint(self, header, name, message, nline=False):
        char = ''
        if nline:
            char = '\n'
        return '{3}{0} ({1}) {2}'.format(
            padding('[{0}]:'.format(header), 20),
            name,
            message,
            char
            )

    def logm(self, message, mode=0, colour='RED'):
        if mode < self.log_level:
            printc(
                self._sprint(message[0], message[1], message[3]),
                getattr(self.colour, colour)
            )

    def logc(self, header, name, message, mode=0, colour='RED'):
        if mode < self.log_level:
            printc(
                self._sprint(header, name, message),
                getattr(self.colour, colour)
            )

    def logn(self, header, name, message, mode=0, colour='RED'):
        if mode < self.log_level:
            printc(
                self._sprint(header, name, message, True),
                getattr(self.colour, colour)
            )

    def loge(self, header, name, message, mode=0):
        if mode < self.log_level:
            printc(
                self._sprint(header, name, message),
                self.colours.RED
            )
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

# Functions
# ------------------------------------------------------------------------ 79->
def padding(message, width):
    if len(message) < width:
        message += ' ' * (width - len(message))
    return message

def printc(message, colour):
    endc = '\033[m'
    print('{0}{1}{2}'.format(colour, message, endc))

# Main
# ------------------------------------------------------------------------ 79->
