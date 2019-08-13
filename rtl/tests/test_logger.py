#! /usr/bin/env python
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
"""Pytest module for testing the rtl.common.logger module."""


# Imports
# ------------------------------------------------------------------------ 79->
from unittest import mock
from rtl.common.logger import log


# Const
# ------------------------------------------------------------------------ 79->
DEBUG = True


# Functions
# ------------------------------------------------------------------------ 79->
@mock.patch('rtl.common.logger.DEBUG', DEBUG)
def test_log(capsys):
    """Test log message for debug mode.

    Args:
        capsys (class): System IO capture class.

    """
    log('this is a test')
    out, _ = capsys.readouterr()
    assert out == '\x1b[38;5;1mthis is a test\x1b[m\n'


# Main
# ------------------------------------------------------------------------ 79->
