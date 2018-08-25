[![Build Status](https://travis-ci.com/kelceydamage/rtl.svg?branch=master)](https://travis-ci.com/kelceydamage/rtl)

![logo](https://github.com/kelceydamage/rtl/blob/master/docs/logo.png?raw=true)

# RASPI Transport Layer

## Documentation Links

* [datatypes](https://github.com/kelceydamage/rtl/blob/master/DATATYPES.md)
* [dependancies](https://github.com/kelceydamage/rtl/blob/master/DEPENDANCIES.md)
* [development](https://github.com/kelceydamage/rtl/blob/master/DEVELOPMENT.md)

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

## Using The Client

```
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
