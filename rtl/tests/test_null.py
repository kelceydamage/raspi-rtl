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
"""Pytest module for testing the rtl.tasks.null module."""


# Imports
# ------------------------------------------------------------------------ 79->
import numpy as np
from rtl.tasks.null import null


# Functions
# ------------------------------------------------------------------------ 79->
def test_null_task():
    """Test valid module name"""
    result = null({}, np.array([1, 2, 3]))
    assert result.tobytes() == np.array([1, 2, 3]).tobytes()


# Main
# ------------------------------------------------------------------------ 79->
