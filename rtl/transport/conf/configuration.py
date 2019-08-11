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
Dependancies:

"""

# Imports
# ------------------------------------------------------------------------ 79->

# Globals
# ------------------------------------------------------------------------ 79->
PIDFILES = '~/var/run/'
TASK_LIB = 'rtl.tasks.*'

# Logging
DEBUG = False
PROFILE = False

# Workers
STARTING_PORT = 10000
# Worker processes per node (per physical # server)
TASK_WORKERS = 3
CACHE_WORKERS = 0
PLOT_WORKERS = 1
PLOT_LISTEN = 5006
PLOT_ADDR = '0.0.0.0'

# Controls the rate at which tasks are sent to the workers, and in doing so,
# the size of the queue.
# Example:
#       1000 req @0.01 = ~100 tasks per queue
#       1000 reg @0.001 = ~10 tasks per queue
# A higher response time increases throughput at the cost of the systems
# responsiveness.
RESPONSE_TIME = 0.005

# Router
RELAY_LISTEN = '0.0.0.0'
RELAY_ADDR = '127.0.0.1'
RELAY_RECV = 19000
RELAY_SEND = 19001
RELAY_PUBLISHER = 19300

# Chunking determines if and how much the router breaks up queues in order
# the better balance worker loads.
# Example:
#       chunking = 10 will break up all queues int ~ 10 tasks per worker.
#       This will negativly affect response time since it adds delay at the
#       router, and extra network activity.
# RESPONSE_TIME and CHUNKING should be balanced to get an Optimal throughput
# and worker load balance.
CHUNKING = True
CHUNKING_SIZE = 1000000

# Cache
CACHE_LISTEN = '0.0.0.0'
CACHE_ADDR = '127.0.0.1'
CACHE_RECV = 19002
CACHE_PATH = '/tmp/transport'
# 512NB for embedded systems
CACHE_MAP_SIZE = 512*1024**2

CACHED = False


# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
