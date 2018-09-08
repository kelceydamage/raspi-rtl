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

A note on overhead and scalability, increasing the chunk size by 1000x increased throughput by 395x. This is mainly due to the opperation performed (sum). There is no benefit in parallelization of an operation optimized for a tight loop, and adding more distribution overhead to such tasks has massive reprecutions. However, bundled tasks do perform better as a rule. While there will be a need to send small commands such as directional/movement controls, the real capability in in processing massive ammounts of signal data. The forthcoming DataNodes will be publishers/processors of sensor data.

There is still a lot of optimizations I can perform based on tht results below.

### Setup 1 (Chunk size: 10000) 0.0753 s/chunk, 13.28 chunks/s, 132,802 operations/s

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
[dispatcher]                    * send()                        3766.35838100 s           10
[dispatcher]                    * _recieve()                    3715.81669600 s           10
[node]                          * recv()                        118.04933366 s            2000
[registry]                      * load_tasks()                  27.68346000 s             4
[relay]                         * receive()                     23.33444788 s             2010
[tasknode]                      * __init__()                    18.39899750 s             4
[cachenode]                     * __init__()                    13.32831000 s             1
[tasknode]                      * run()                         13.09554515 s             2000
[node]                          * __init__()                    9.73731400 s              5
[relay]                         * chunk()                       9.18255240 s              1510
[relay]                         * __init__()                    6.33697000 s              1
[task_sum]                      * task_sum()                    2.80779358 s              2000
[relay]                         * assemble()                    1.35952374 s              500
[relay]                         * empty_cache()                 0.93393400 s              10
[node]                          * send()                        0.57681933 s              2000
[cache]                         * __init__()                    0.47109717 s              4050
[relay]                         * ship()                        0.43799093 s              2000
[dispatcher]                    * __init__()                    0.28577300 s              10
[cache]                         * sync()                        0.21387800 s              10
[cachenode]                     * load_database()               0.11729000 s              1
[relay]                         * create_state()                0.01037836 s              500
[relay]                         * retrieve_state()              0.00600460 s              500
[node]                          * consume()                     0.00526189 s              2000
```

### Setup 12(Chunk size: 10) 0.0298 s/chunk, 33.56 chunks/s, 335.6 operations/s

* Task operations: 5000
* Job runs: 1
* Task nodes: 4
* Cores: 1
* i7-7820HQ CPU @ 2.90GHz
* Ram: 512 MB

```
RANKED

Class                           Method                          per 1000 calls            count
----------------------------------------------------------------------------------------------------
[dispatcher]                    * send()                        16754.65632000 s          1
[dispatcher]                    * _recieve()                    16751.63486000 s          1
[tasknode]                      * __init__()                    27.58852500 s             4
[node]                          * recv()                        22.86703347 s             2000
[registry]                      * load_tasks()                  22.09832250 s             4
[node]                          * __init__()                    12.45389800 s             5
[cachenode]                     * __init__()                    11.40730000 s             1
[tasknode]                      * run()                         5.28934333 s              2000
[relay]                         * chunk()                       4.24201905 s              1501
[relay]                         * __init__()                    4.05777000 s              1
[relay]                         * receive()                     3.47492400 s              2001
[relay]                         * empty_cache()                 3.16290000 s              1
[cache]                         * sync()                        2.46841000 s              1
[relay]                         * assemble()                    0.75060228 s              500
[cache]                         * __init__()                    0.49802226 s              4014
[dispatcher]                    * __init__()                    0.27867000 s              1
[cachenode]                     * load_database()               0.15292000 s              1
[node]                          * send()                        0.07388488 s              2000
[relay]                         * ship()                        0.06444775 s              2000
[task_sum]                      * task_sum()                    0.00918006 s              2000
[relay]                         * create_state()                0.00639448 s              500
[relay]                         * retrieve_state()              0.00542992 s              500
[node]                          * consume()                     0.00528747 s              2000
```
