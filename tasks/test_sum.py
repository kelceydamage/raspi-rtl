#!/usr/bin/env python
# ------------------------------------------------------------------------ 79->
# Author: ${name=Kelcey Damage}
# Python: 3.5+
# Doc
# ------------------------------------------------------------------------ 79->
# Dependancies:
#

# Imports
# ------------------------------------------------------------------------ 79->
from tasks.sum import *

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def test_sum(): # pragma: no cover
    assert task_sum({'worker': 9999, 'data': [[1, 2, 3, 4]]}) == [[10]]

# Main
# ------------------------------------------------------------------------ 79->
