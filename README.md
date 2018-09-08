[![Build Status](https://travis-ci.com/kelceydamage/rtl.svg?branch=master)](https://travis-ci.com/kelceydamage/rtl) [![Coverage Status](https://coveralls.io/repos/github/kelceydamage/rtl/badge.svg)](https://coveralls.io/github/kelceydamage/rtl) [![codecov](https://codecov.io/gh/kelceydamage/rtl/branch/master/graph/badge.svg)](https://codecov.io/gh/kelceydamage/rtl) [![Code Health](https://landscape.io/github/kelceydamage/rtl/master/landscape.svg?style=flat)](https://landscape.io/github/kelceydamage/rtl/master) [![Maintainability](https://api.codeclimate.com/v1/badges/05de3d7d075c1ca48b1a/maintainability)](https://codeclimate.com/github/kelceydamage/rtl/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/05de3d7d075c1ca48b1a/test_coverage)](https://codeclimate.com/github/kelceydamage/rtl/test_coverage)

![logo](https://github.com/kelceydamage/rtl/blob/master/docs/logo.png?raw=true)

# RASPI Transport Layer v0.3

## Documentation Links

* [datatypes](https://github.com/kelceydamage/rtl/blob/master/DATATYPES.md)
* [dependancies](https://github.com/kelceydamage/rtl/blob/master/DEPENDANCIES.md)
* [development](https://github.com/kelceydamage/rtl/blob/master/DEVELOPMENT.md)

## Communication Diagram

![logo](https://github.com/kelceydamage/rtl/blob/master/docs/msg-diag.png?raw=true)

The transport layer is comprised of 3 main components:

#### Relay
The relay is the primary coordinator for forwarding, splitting, and assembling work requests. The role of the relay is to ensure pipeline stages are assigned to tasknodes, and completed pipelines are returned to the requestor.

#### TaskNode
The tasknode processes a given stage in the pipeline. If a stage exists in the task library, it is executed over the accompanying data, and the result is returned to the relay.

#### CacheNode
The cachenode was originally designed to store repetitive REST queries to external services, but can also store and age out any type of data that can be represented as a key, value pair.

## Usage

To start the service:
```
./transport/bin/start.sh
```

To stop the service:
```
./transport/bin/kill.sh
```

## Ports

| Service   | Function    | Port  |
|-----------|-------------|-------|
|Relay      | Recieve     | 19000 |
|           | Send        | 19001 |
|           | Publish     | 19300 |
|Dispatcher | Send        |*      |
|           | Subscribe   |*      |
|TaskNode   | Recieve     |*      |
|           | Send        |*      |
|CacheNode  | Router      | 19002 |

## Settings (configuration.py)

| Setting | Value | Description |
|---------|-------|-------------|
|LOG_LEVEL| 3     |             |
|PROFILE  | False | Turn on profiler. Logs are stored in var/log/performance.log |
|STARTING_PORT| 10000|          |
|TASK_WORKERS | 3 | Worker processes per node (per physical server) |
|CACHE_WORKERS | 1 |            |
|RESPONSE_TIME | 0.005 | Controls the rate at which tasks are sent to the workers, and in doing so, the size of the queue. A higher response time increases throughput at the cost of the systems responsiveness. |
|RELAY_LISTEN | '0.0.0.0' |     |
|RELAY_ADDR   | '127.0.0.1' |   |
|RELAY_RECV   | 19000       |   |
|RELAY_SEND   | 19001       |   |
|RELAY_PUBLISHER | 19300    |   |
|CHUNKING     | True | Chunking determines if and how much the router breaks up queues in order the better balance worker loads. RESPONSE_TIME and CHUNKING should be balanced to get an Optimal throughput and worker load balance.|
|CHUNKING_SIZE | 500 |          |
|CACHE_LISTEN | '0.0.0.0' | |
|CACHE_ADDR   | '127.0.0.1' |   |
|CACHE_RECV   | 19002 |         |
|CACHE_PATH   | '/tmp/transport' | This is where the general cache is stored. |
|CACHE_MAP_SIZE | 512*1024**2 | 512MiB to start. |
|CACHED       | False | Determines if the inter-task data will be cached or transmitted. Transmition is usually the fasted method. |

## Creating A Job
```python
# Import the datatypes
from common.datatypes import *

# Create envelope
envelope = Envelope()

# Create meta
meta = Meta()

# Create pipeline
pipeline = Pipeline()
pipeline.tasks = ['task_sum', 'task_sum', 'task_sum', 'task_sum']

# Create data
data = [[1, 2, 3], [2, 3 ,4], [5, 3 ,4], [1, 2, 3]]

# Create header
header = Tools.create_id()

# Pack the envelope
envelope.pack(header, meta.extract(), pipeline.extract(), data)

```

## Using The Client

```python
# Import the Dispatcher
from transport.dispatch import Dispatcher

# Dispatch envelope
envelope = dispatcher.send(envelope)
```

## Code Performance Numbers (Incl Sum Task)

Profiler adds about 12.7% overhead. The dispatcher calls are round-trip time, all other calls are affected by chunk size.

A note on overhead and scalability, increasing the chunk size by 1000x increased performance by 33.3x. Bundled tasks perform better as a rule. While there will be a need to send small commands such as directional/movement controls, the real capability in in processing massive ammounts of signal data. The forthcoming DataNodes will be publishers/processors of sensor data.

### Setup 1 (Chunk size: 10000) 0.09312 s/chunk, 10.74 chunks/s, 107,388 operations/s

* Task operations: 500000
* Job runs: 10
* Task nodes: 4
* Cores: 1
* i7-7820HQ CPU @ 2.90GHz
* Ram: 512 MB

```
RANKED

Class                           Method                          per 1000 calls            count
----------------------------------------------------------------------------------------------------
[dispatcher]                    * send()                        4656.04377200 s           10
[dispatcher]                    * _recieve()                    4609.08972200 s           10
[node]                          * recv()                        193.55175365 s            2000
[relay]                         * receive()                     40.03844415 s             2010
[tasknode]                      * run()                         13.68467270 s             2000
[relay]                         * chunk()                       11.73567601 s             1510
[task_sum]                      * task_sum()                    2.50302514 s              2000
[relay]                         * assemble()                    1.59859166 s              500
[relay]                         * empty_cache()                 1.12340600 s              10
[node]                          * send()                        1.00808554 s              2000
[relay]                         * ship()                        0.85979777 s              2000
[cache]                         * __init__()                    0.50517393 s              4040
[dispatcher]                    * __init__()                    0.28822700 s              10
[cache]                         * sync()                        0.21364300 s              10
[relay]                         * create_state()                0.01066204 s              500
[relay]                         * retrieve_state()              0.00722248 s              500
[node]                          * consume()                     0.00535370 s              2000
```

### Setup 12(Chunk size: 10) 0.0031 s/chunk, 322.58 chunks/s, 3,226 operations/s

* Task operations: 500000
* Job runs: 1
* Task nodes: 4
* Cores: 1
* i7-7820HQ CPU @ 2.90GHz
* Ram: 512 MB

```
RANKED

Class                           Method                          per 1000 calls            count
----------------------------------------------------------------------------------------------------
[dispatcher]                    * send()                        155771.76270909 s         11
[dispatcher]                    * _recieve()                    155724.66497636 s         11
[registry]                      * load_tasks()                  25.66331375 s             8
[node]                          * recv()                        20.35494002 s             202000
[tasknode]                      * __init__()                    18.18360750 s             8
[cachenode]                     * __init__()                    10.41176500 s             2
[node]                          * __init__()                    8.36317400 s              10
[tasknode]                      * run()                         5.57752955 s              202000
[relay]                         * chunk()                       4.46224174 s              151511
[relay]                         * __init__()                    4.01119500 s              2
[relay]                         * receive()                     2.44436271 s              202011
[relay]                         * empty_cache()                 1.09168909 s              11
[relay]                         * assemble()                    0.68624944 s              50500
[cache]                         * __init__()                    0.50200265 s              404064
[dispatcher]                    * __init__()                    0.28562273 s              11
[cache]                         * sync()                        0.20734364 s              11
[cachenode]                     * load_database()               0.15399500 s              2
[node]                          * send()                        0.08371161 s              202000
[relay]                         * ship()                        0.07720226 s              202000
[task_sum]                      * task_sum()                    0.03211160 s              202000
[relay]                         * create_state()                0.00824853 s              50500
[node]                          * consume()                     0.00543692 s              202000
[relay]                         * retrieve_state()              0.00506232 s              50500
```
