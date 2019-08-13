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
Attributes:
    PIDFILES (str): Location to store pid files.

        - Default: ``'~/var/run/'``
    TASK_LIB (str): Module name for tasks library.

        - Default: ``'rtl.tasks.*'``
    DEBUG (bool): True to enable debug printing, else False to prevent.

        - Default: ``False``
    PROFILE (bool): True to enable timings, else False to prevent.

        - Default: ``False``
    STARTING_PORT (int): Port block for workers to consume.

        - Default: ``10000``
    TASK_WORKERS (int): The number of task workers to spawn.

        - Default: ``3``
    PLOT_WORKERS (int): The number of plot workers to spawn.

        - Default: ``1``
        Danger:
            Setting this above 1 could have unexpected behaviors.
    PLOT_LISTEN (int): The port on which to server plots.

        - Default: ``5006``
    PLOT_ADDR (str): The IP address that the plot worker will listen on.

        - Default: ``'0.0.0.0'``

    RESPONSE_TIME (float): Controls the rate at which tasks are sent to the
        workers, and in doing so, the size of the queue.

        Examples:

            1000 req @0.01 = ~100 tasks per queue.

            1000 reg @0.001 = ~10 tasks per queue.

        - Default: ``0.005``

    RELAY_LISTEN (str): The IP address that the relay worker will listen on.

        - Default: ``'0.0.0.0'``
    RELAY_ADDR (str): The IP address that relay client will connect to.

        - Default: ``'127.0.0.1'``
    RELAY_RECV (int): The recieve port on the relay worker.

        - Default: ``19000``
    RELAY_SEND (int): The send port on the relay worker.

        - DefaultL ``19001``
    RELAY_PUBLISHER (int): The publisher port on the relay worker.

        - Default: ``19300``
    CHUNKING (bool): Enable chunking service on the relay worker.

        Important:
            Chunking determines if and how much the router breaks up queues in
            order the better balance worker loads.

        Examples:

            A setting of 10 will break up all queues int ~ 10 tasks per worker.
            This will negativly affect response time since it adds delay at the
            router, and extra network activity.

        Note:
            RESPONSE_TIME and CHUNKING should be balanced to get an Optimal
            throughput and worker load balance.

        - Default: ``True``
    CHUNKING_SIZE (int): The desired size of each chunk.

        - Default: ``1000000``
    CACHE_PATH (str): The path to store the cache file.

        - Default: ``'/tmp/transport'``

    CACHE_MAP_SIZE (int): The size of the cache (memory allocation) for the
        task cache.

        Note:
            The default value is 512MB for embedded systems

        - Default: ``512*1024**2``

"""

# Imports
# ------------------------------------------------------------------------ 79->

# Globals
# ------------------------------------------------------------------------ 79->
# [Infrastructure]
PIDFILES = '~/var/run/'
TASK_LIB = 'rtl.tasks.*'
CACHE_PATH = '/tmp/transport'
CACHE_MAP_SIZE = 512*1024**2
RESPONSE_TIME = 0.005
CHUNKING_SIZE = 1000000
CHUNKING = True

# [Logging]
DEBUG = False
PROFILE = False

# [Task Workers]
STARTING_PORT = 10000
TASK_WORKERS = 3

# [Plot Workers]
PLOT_WORKERS = 1
PLOT_LISTEN = 5006
PLOT_ADDR = '0.0.0.0'

# [Relay Workers]
RELAY_LISTEN = '0.0.0.0'
RELAY_ADDR = '127.0.0.1'
RELAY_RECV = 19000
RELAY_SEND = 19001
RELAY_PUBLISHER = 19300


# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
