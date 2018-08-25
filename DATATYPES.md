[home](https://github.com/kelceydamage/rtl/blob/master/README.md)
# Datatypes

## Envelopes

Envelopes are the primary container used to send messages throughout the transport layer. Envelopes comprise four components, and are capped at a length of 4. At their core, envelopes are deques.

The four parts in order of porsition are: `header`, `meta`, `pipeline`, and `data`.

#### Using Envelopes
There are two ways to populate an envelope:
```
Envelope.pack(header, meta, pipeline, data)
```
This method requires raw python datastructs to populate. Header is a `uuid`, meta is a `dict`, pipeline is a `dict`, and data is a `list`. This method is primarily used to create new envelopes, or repack and unpacked envelope.

```
Envelope.load(sealed_envelope)
```
This method requires an pre serialized sealed_envelope, such as would arrive via a socket.

### Attributes

* lifespan
* length
* size

#### Size
```
type: int
```
The size in bytes of the `data` payload.

#### Length
```
type: int
```
The number of items in the `data` payload.

#### Lifespan
```
type: int
```
The number of remaining tasks in the pipeline.

## Meta

### Attributes

* size
* length
* lifespan
* times
* stage

#### Size
```
type: int
```
The size in bytes of the `data` payload.

#### Length
```
type: int
```
The number of items in the `data` payload.

#### Lifespan
```
type: int
```
The number of remaining tasks in the pipeline.

#### Times
```
type: dict
```
Holder for timing floats (not really used).

#### Stage
```
type: uuid
```
The serial number for the segments generated when an envelope in split up in the chunker.

## Pipelines

### Attributes

* tasks
* completed
* kwargs

#### Tasks
```
type: deque
```
The pending tasks in a pipeline.

#### Completed
```
type: deque
```
Holds an entry for each completed task.

#### Kwargs
```
type: dict
```
All the values required for tasks in the pipeline that are not `data`.
