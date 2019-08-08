[![Build Status](https://travis-ci.com/kelceydamage/rtl.svg?branch=master)](https://travis-ci.com/kelceydamage/rtl) 
[![Coverage Status](https://coveralls.io/repos/github/kelceydamage/rtl/badge.svg)](https://coveralls.io/github/kelceydamage/rtl) 
[![codecov](https://codecov.io/gh/kelceydamage/rtl/branch/master/graph/badge.svg)](https://codecov.io/gh/kelceydamage/rtl) 
[![Code Health](https://landscape.io/github/kelceydamage/rtl/master/landscape.svg?style=flat)](https://landscape.io/github/kelceydamage/rtl/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/05de3d7d075c1ca48b1a/maintainability)](https://codeclimate.com/github/kelceydamage/rtl/maintainability) 
[![Test Coverage](https://api.codeclimate.com/v1/badges/05de3d7d075c1ca48b1a/test_coverage)](https://codeclimate.com/github/kelceydamage/rtl/test_coverage)

![logo](https://github.com/kelceydamage/rtl/blob/master/docs/logo.png?raw=true)

# RASPI Transport Layer v3-experimental
## Documentation Links

* [datatypes](https://github.com/kelceydamage/rtl/blob/master/DATATYPES.md)
* [dependancies](https://github.com/kelceydamage/rtl/blob/master/DEPENDANCIES.md)
* [development](https://github.com/kelceydamage/rtl/blob/master/DEVELOPMENT.md)

## Functionality
### Included Tasks
* add
* aggregate
* average
* cross average
* static classifier
* column space
* divide
* filter
* histogram
* log
* cross max
* multiply
* normalize
* open
* array open
* power
* regression
* plot
* sort
* square root
* subtract
* unique
* array write

## Usage
### RTL Platform

To start the service:
```
./transport/bin/init.sh start
```

To stop the service:
```
./transport/bin/init.sh stop
```

There are also `status` and `restart` commands.

### Using The Built-in Client

```python
# Import the Transform engine
from common.transform import Transform

# Write your DSDSL
DSDSL = {
    0: {
        'tasks': {
            'task_open_array': {
                'filename': FILENAME,
                'path': 'raw_data',
                'extension': 'dat',
                'delimiter': None
            }
        }
    }
}

# Feed your DSDSL to the execute() function and call result()
r = Transform().execute(DSDSL).result()
```

### Creating A Client ()
```python
# Import the datatypes, dispatcher, and cache
from common.datatypes import Envelope
from transport.dispatch import Dispatcher
from transport.cache import Cache
import cbor

# Create and instance of the three imports
envelope = Envelope()
dispatcher = Dispatcher()
cache = Cache()

# Write your DSDSL
DSDSL = {
    0: {
        'tasks': {
            'task_open_array': {
                'filename': FILENAME,
                'path': 'raw_data',
                'extension': 'dat',
                'delimiter': None
            }
        }
    }
}

# init the envelope
envelope.pack(1)

# Stash the schema wo the worker nodes can access it. We use the 
# envelopes ID since it is a UUID and unique, we also encode the 
# schema as bytes. Most importantly we only cache one stage per 
# envelope: DSDSL[0] in this case.
cache.put(envelope.getId(), cbor.dumps(DSDSL[0]))

# run the job
result = dispatcher.send(envelope)
```

### Sample Job Run
```python
(python3) [vagrant@localhost rtl]$ python dsdsl/dev.py
Failed to load CuPy falling back to Numpy
Running: 0 - b'a67269ef-4c31-4d28-ab1b-1da6bc0ca246'
Running: open_array
Completed: 1.98 ms open_array
Running: 1 - b'9f6cf43b-1b05-4fb5-9d3c-5faee0e0c70a'
Running: filter
=> Filtered Results: (51461,)
=> Filtered Results: (403,)
=> Filtered Results: (33,)
=> Filtered Results: (33,)
Completed: 3.47 ms filter
Running: add
Completed: 0.18 ms add
Running: divide
Completed: 0.12 ms divide
Running: normalize
=> totalRunTime : MAX 4580781.5 MIN 35340.0 AVG 2290390.75 COUNT 33
=> totalReadBytes : MAX 1402596224.0 MIN 390932.0 AVG 701298112.0 COUNT 33
=> concurrentRunTime : MAX 225545.28125 MIN 8224.2861328125 AVG 112772.640625 COUNT 33
=> concurrentReadBytes : MAX 77283224.0 MIN 56666.14453125 AVG 38641612.0 COUNT 33
Completed: 0.41 ms normalize
Running: subtract
Completed: 0.16 ms subtract
Running: average
Completed: 0.17 ms average
Running: simple_plot
Completed: 0.10 ms simple_plot
Total Elapsed Time: 0.03805337700032396
```

## Architecture
### Communication Diagram

![logo](https://github.com/kelceydamage/rtl/blob/master/docs/msg-diag.png?raw=true)

The transport layer is comprised of 3 main components:

#### Relay
The relay is the primary coordinator for forwarding, splitting, and assembling work requests. The role of the relay is to ensure pipeline stages are assigned to tasknodes, and completed pipelines are returned to the requestor.

#### TaskNode
The tasknode processes a given stage in the pipeline. If a stage exists in the task library, it is executed over the accompanying data, and the result is returned to the relay.

#### PlotNode
The plotnode runs a bokeh server and allows you to create visualizations right from the DSDSL.

### Ports

| Service   | Function    | Port  |
|-----------|-------------|-------|
|Relay      | Recieve     | 19000 |
|           | Send        | 19001 |
|           | Publish     | 19300 |
|Dispatcher | Send        |*      |
|           | Subscribe   |*      |
|TaskNode   | Recieve     |*      |
|           | Send        |*      |
|PlotNode   | Router      | 5006  |

## Configuration
### Settings (configuration.py)

| Setting | Value | Description |
|---------|-------|-------------|
|DEBUG| False     | Enables method tracing |
|PROFILE  | False | prints timings epochs for analysis of internode performance |
|STARTING_PORT| 10000|          |
|TASK_WORKERS | 3 | Worker processes per node (per physical server) |
|CACHE_WORKERS | 1 |            |
|PLOT_WORKWERS | 1 |            |
|PLOT_LISTEN   | 5006 |            |
|PLOT_ADDR     | '0.0.0.0' |            |
|RESPONSE_TIME | 0 | Controls the rate at which tasks are sent to the workers, and in doing so, the size of the queue. A higher response time increases throughput at the cost of the systems responsiveness. uncapped for now |
|RELAY_LISTEN | '0.0.0.0' |     |
|RELAY_ADDR   | '127.0.0.1' |   |
|RELAY_RECV   | 19000       |   |
|RELAY_SEND   | 19001       |   |
|RELAY_PUBLISHER | 19300    |   |
|CHUNKING     | False | Chunking determines if and how much the router breaks up queues in order the better balance worker loads. RESPONSE_TIME and CHUNKING should be balanced to get an Optimal throughput and worker load balance.|
|CHUNKING_SIZE | 1000000 |          |
|CACHE_PATH   | '/tmp/transport' | This is where the general cache is stored. |
|CACHE_MAP_SIZE | 512*1024**2 | 512MiB to start. |

## Performance
### Code Performance Numbers

A note on overhead and scalability, there is no benefit in parallelization of an operation optimized for a tight loop, and adding more distribution overhead to such tasks has massive repercussions. However, bundled tasks do perform better as a rule. While there will be a need to send small commands such as directional/movement controls, the real capability is in processing massive ammounts of signal data. The forthcoming DataNodes will be publishers/processors of sensor data.

* peak binary file streaming ~5 GB/s
* peak tabular file streaming ~330 MB/S
* simple math operations on datasets ~0.2 ms
* sending large tables(15 MB) between nodes ~5-7 ms
* zmq overhead(latency) ~1 ms
* platform overhead(latency) ~2 ms

Currently all tasks in a single stage will be executed on the same task node to allow reusability of both the data and the state. This avoide going back to the router between tasks. Different stages will execute in a dealer pattern, but any stages comming from the same transform will not execute in parallel (yet).

Finally, task splitting was removed until it can be re-implemented in a performant way.

