[![Build Status](https://travis-ci.com/kelceydamage/rtl.svg?branch=master)](https://travis-ci.com/kelceydamage/rtl) [![Coverage Status](https://coveralls.io/repos/github/kelceydamage/rtl/badge.svg)](https://coveralls.io/github/kelceydamage/rtl) [![codecov](https://codecov.io/gh/kelceydamage/rtl/branch/master/graph/badge.svg)](https://codecov.io/gh/kelceydamage/rtl) [![Code Health](https://landscape.io/github/kelceydamage/rtl/master/landscape.svg?style=flat)](https://landscape.io/github/kelceydamage/rtl/master) [![Maintainability](https://api.codeclimate.com/v1/badges/05de3d7d075c1ca48b1a/maintainability)](https://codeclimate.com/github/kelceydamage/rtl/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/05de3d7d075c1ca48b1a/test_coverage)](https://codeclimate.com/github/kelceydamage/rtl/test_coverage)

![logo](https://github.com/kelceydamage/rtl/blob/master/docs/logo.png?raw=true)

# RASPI Transport Layer v0.2

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
|CACHE_ADDR   | '127.0.0.1' |   |
|CACHE_RECV   | 19002 |         |

## Using The Client

```python
from transport.dispatch import Dispatcher
from common.datatypes import *

# Create a dispatcher
dispatcher = Dispatcher()

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

# Dispatch envelope
envelope = dispatcher.send(envelope)
```
