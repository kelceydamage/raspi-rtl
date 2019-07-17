[![Build Status](https://travis-ci.com/kelceydamage/rtl.svg?branch=master)](https://travis-ci.com/kelceydamage/rtl) 
[![Coverage Status](https://coveralls.io/repos/github/kelceydamage/rtl/badge.svg)](https://coveralls.io/github/kelceydamage/rtl) 
[![codecov](https://codecov.io/gh/kelceydamage/rtl/branch/master/graph/badge.svg)](https://codecov.io/gh/kelceydamage/rtl) 
[![Code Health](https://landscape.io/github/kelceydamage/rtl/master/landscape.svg?style=flat)](https://landscape.io/github/kelceydamage/rtl/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/05de3d7d075c1ca48b1a/maintainability)](https://codeclimate.com/github/kelceydamage/rtl/maintainability) 
[![Test Coverage](https://api.codeclimate.com/v1/badges/05de3d7d075c1ca48b1a/test_coverage)](https://codeclimate.com/github/kelceydamage/rtl/test_coverage)

![logo](https://github.com/kelceydamage/rtl/blob/master/docs/logo.png?raw=true)

# RASPI Transport Layer v2.1a

## Documentation Links

* [datatypes](https://github.com/kelceydamage/rtl/blob/master/DATATYPES.md)
* [dependancies](https://github.com/kelceydamage/rtl/blob/master/DEPENDANCIES.md)
* [development](https://github.com/kelceydamage/rtl/blob/master/DEVELOPMENT.md)

# Included Tasks
* add
* average
* cross average
* static classifier
* column space
* divide
* filter
* multiply
* normalize
* open
* array open
* regression
* plot
* sort
* subtract
* array write

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

#### RTL Platform

To start the service:
```
./transport/bin/init.sh start
```

To stop the service:
```
./transport/bin/init.sh stop
```

There are also `status` and `restart` commands.

#### Sample Job Run
```python
-------------------------------------------------------------------------------
Running Stage: [1]
* task_open_file
* task_custom_convert_to_numeric
JOB COMPLETED: 0.04718806396704167s
-------------------------------------------------------------------------------
Running Stage: [2]
* task_end
JOB COMPLETED: 0.004064688924700022s
[(b'd9cc2ba0-5d56-498f-8ae1-3cb2dd46ae87', 0, 1033, 9)]
-------------------------------------------------------------------------------
[[                  0          1557331619                   1 ...
                  201                 505                  55]
 [                  1          1557330853                   1 ...
                  785               12221                 262]
 [                  2          1557330687                   2 ...
                  543                3647                   5]
 ...
 [               1030          1557256349                   1 ...
                 2586               17974                  33]
 [               1031          1557255192                   5 ...
                   39                  63                   3]
 [3546410301743260984 3471493771197290616 4195157290668535093 ...
  3776322582150998898 7004280740711444790 4050261328960709428]]
[(b'd9cc2ba0-5d56-498f-8ae1-3cb2dd46ae87', 0, 1033, 9)]
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
from common.datatypes import Envelope

# Create envelope
envelope = Envelope()

# Determine pipeline
tasks = ['task_multiply', 'task_multiply']

# Create meta
meta={'tasks': tasks, 'completed': [], 'kwargs': {}}

# Create data
data = [[1.0, 2.0, 3.0] for i in range(500000)]

# Pack the envelope
envelope.pack(meta=meta, ndata=data)
```

## Using The Client

```python
# Import the Dispatcher
from transport.dispatch import Dispatcher

# Dispatch envelope
envelope = dispatcher.send(envelope)
```

## Getting The Result

```python
# Result is an ndarray
_ndarray = envelope.result()
```

## Code Performance Numbers (Incl Sum Task)

A note on overhead and scalability, there is no benefit in parallelization of an operation optimized for a tight loop, and adding more distribution overhead to such tasks has massive repercussions. However, bundled tasks do perform better as a rule. While there will be a need to send small commands such as directional/movement controls, the real capability is in processing massive ammounts of signal data. The forthcoming DataNodes will be publishers/processors of sensor data.

### 0.00955 s/chunk, 104.71 chunks/s, 523,560 arrays/s, 2,094,240 operations/s

* Data objects: 500000
* Chunk size: 5000
* Task operations: 4
* Job runs: 10
* Task nodes: 3
* Cores: 3
* i7-7820HQ CPU @ 2.90GHz
* Ram: 2048 MB

### Benchmark Linear loop main thread 4 tasks (3 core VM) (2 million operations)
```
data.setflags(write=1)
for i in range(len(tasks)):
    for i in range(data.shape[0]):
        data[i] = np.multiply(data[i], data[i])
```
500000 * 4 Multiplies took: 2.44180964s

### Benchmark 3 RTL workers nodes 4 tasks (3 core VM) (2 million operations)
```
data.setflags(write=1)
for i in range(data.shape[0]):
    data[i] = np.multiply(data[i], data[i])
```
500000 * 4 Multiplies took: 0.9547774170059711s

