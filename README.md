[![Build Status](https://travis-ci.com/kelceydamage/rtl.svg?branch=master)](https://travis-ci.com/kelceydamage/rtl) [![Coverage Status](https://coveralls.io/repos/github/kelceydamage/rtl/badge.svg)](https://coveralls.io/github/kelceydamage/rtl) [![codecov](https://codecov.io/gh/kelceydamage/rtl/branch/master/graph/badge.svg)](https://codecov.io/gh/kelceydamage/rtl) [![Code Health](https://landscape.io/github/kelceydamage/rtl/master/landscape.svg?style=flat)](https://landscape.io/github/kelceydamage/rtl/master) [![Maintainability](https://api.codeclimate.com/v1/badges/05de3d7d075c1ca48b1a/maintainability)](https://codeclimate.com/github/kelceydamage/rtl/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/05de3d7d075c1ca48b1a/test_coverage)](https://codeclimate.com/github/kelceydamage/rtl/test_coverage)

![logo](https://github.com/kelceydamage/rtl/blob/master/docs/logo.png?raw=true)

# RASPI Transport Layer v0.4

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

A note on overhead and scalability, increasing the chunk size by 1000x increased throughput by 358x. This is mainly due to the opperation performed (sum). There is no benefit in parallelization of an operation optimized for a tight loop, and adding more distribution overhead to such tasks has massive reprecutions. However, bundled tasks do perform better as a rule. While there will be a need to send small commands such as directional/movement controls, the real capability in in processing massive ammounts of signal data. The forthcoming DataNodes will be publishers/processors of sensor data.

There is still a lot of optimizations I can perform based on tht results below.

### Setup 1 (Chunk size: 10000) 0.0277 s/chunk, 36.10 chunks/s, 361,011 operations/s

* Task operations: 500000
* Job runs: 10
* Task nodes: 3
* Cores: 3
* i7-7820HQ CPU @ 2.90GHz
* Ram: 2048 MB

### Benchmark Linear loop main thread (3 core VM)

Envelope Length: 500000
JOB COMPLETED: 1.543776273727417s
```
r = []
while data:
    x = data.pop()
    r.append([numpy.multiply(x, x).tolist()])
```
500000 Multiplies took: 1.6345291137695312s

### Benchmark 3 RTL workers nodes (3 core VM)
```
results = []
while kwargs['data']:
    x = kwargs['data'].pop()
    results.append(numpy.multiply(x, x).tolist())
```
500000 Multiplies took: 1.3850457668304443s (Profiling turned off)

#### Call Times (Profiling turned on):

```
RANKED

Class                           Method                          per 1000 calls            count
----------------------------------------------------------------------------------------------------
[dispatcher]                    * send()                        1970.81692000 s           1
[dispatcher]                    * _recieve()                    1915.37958000 s           1
[relay]                         * chunk()                       884.88298000 s            1
[node]                          * recv_loop()                   814.82893320 s            50
[relay]                         * recv_loop()                   252.56732510 s            51
[tasknode]                      * run()                         37.41902600 s             50
[task_multiply]                 * task_multiply()               32.25967940 s             50
[relay]                         * load_envelope()               11.49281882 s             51
[node]                          * load_envelope()               9.22512980 s              50
[node]                          * send()                        7.11619520 s              50
[relay]                         * send()                        6.62053920 s              50
[relay]                         * assemble()                    1.83960780 s              50
[encoding]                      * deserialize()                 1.71853939 s              408
[relay]                         * empty_cache()                 0.75265000 s              1
[cache]                         * __init__()                    0.71184000 s              3
[encoding]                      * serialize()                   0.45578319 s              408
[dispatcher]                    * __init__()                    0.35906000 s              1
[cache]                         * sync()                        0.12727000 s              1
[encoding]                      * create_id()                   0.03023000 s              1
[relay]                         * create_state()                0.00975420 s              50
[relay]                         * retrieve_state()              0.00707340 s              50
[node]                          * consume()                     0.00538760 s              50
```
