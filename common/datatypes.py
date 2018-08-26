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
# Dependancies:
#                   hashlib
#                   base64
#                   ujson
#                   collections
#                   uuid
#                   sys
#                
# Imports
# ------------------------------------------------------------------------ 79->
import hashlib
import base64
import ujson as json
import collections
import uuid
import sys

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->
class Tools(object):
    """
    NAME:           Tools

    DESCRIPTION:    A class of utility functions used by the datatypes.

    METHODS:        .serialize(obj)
                    Converts an object into a bytes encoded serialized object.

                    .deserialize(obj)
                    Converts a bytes encoded serialized object back into an 
                    object.

                    .create_header(meta)
                    Creates a bytes encoded hash(md5) of the metadata.

                    .create_id()
                    Creates a bytes encoded UUID4.
    """
    @staticmethod
    def serialize(obj):
        return base64.b64encode((json.dumps(obj)).encode())

    @staticmethod
    def deserialize(obj):
        return json.loads(base64.b64decode(obj).decode())

    @staticmethod
    def create_header(meta):
        return hashlib.md5(json.dumps(meta).encode()).hexdigest().encode()

    @staticmethod
    def create_id():
        return str(uuid.uuid4()).encode()

class Parcel(object):
    """
    NAME:           Envelope

    DESCRIPTION:    A class of utility functions used by the envelope when 
                    routing, beit dealer or router sockets. It stores an 
                    additional header(route) and a null byte char. Used for
                    sending between routing members of the transport framework.

    METHODS:        .pack(route, envelope)
                    Packs up a header(route) and and envelope into a parcel.

                    .unpack()
                    Unpacks the parcel into both a route and an envelope.

                    .load()
                    Loads the serialized representation of a parcel into a 
                    parcel(obj).

                    .seal()
                    Returns the internal deque as a list.
    """
    def __init__(self):
        self.contents = collections.deque(maxlen=6)
        self.lifespan = 0

    def pack(self, route, envelope):
        self.contents.append(route)
        self.contents.append(b'')
        self.contents.extend(envelope.seal())

    def unpack(self):
        envelope = Envelope()
        envelope.load(list(self.contents)[2:])
        return self.contents[0], envelope

    def load(self, parcel):
        envelope = Envelope()
        envelope.load(parcel[2:])
        self.pack(parcel[0], envelope)

    def seal(self):
        return list(self.contents)

class Envelope(object):
    """
    NAME:           Envelope

    DESCRIPTION:    A class of utility functions used by the datatypes. It 
                    stores a header, meta, pipeline, and data, for sending
                    between members of the transport framework.

    METHODS:        .pack(header, meta, pipeline, data)
                    Packs up a header, meta(obj), pipeline(obj), and data
                    into and envelope(obj).

                    .load(sealed_envelope)
                    Loads the serialized representation of an envelope(obj)
                    into an envelope(obj).

                    .open()
                    Returns the envelope(obj) in it's completely deserialized
                    form.

                    .unpack()
                    Unpacks the envelope(obj) into a header, meta(obj), 
                    pipeline(obj), and data.

                    .seal()
                    Returns the internal deque as a list.

                    .get_header()
                    Returns bytes encoded serialized header.

                    .get_raw_header()
                    Returns the deserialized header.

                    .get_meta()
                    Returns the envelopes deserialized meta(obj).

                    .get_pipeline()
                    Returns the envelopes deserialized pipeline(obj).

                    .get_data()
                    Returns the envelopes deserialized data.

                    .update_data(data)
                    Replace the envelopes data.

                    .update_meta(meta)
                    Replace the envelopes meta.

                    .empty()
                    Clear the envelope.

                    .validate()
                    Validate the envelope length.
    """
    def __init__(self):
        self.contents = collections.deque(maxlen=4)
        self.lifespan = 0

    def pack(self, header, meta, pipeline, data):
        meta['lifespan'] = len(pipeline['tasks'])
        meta['length'] = len(data)
        meta['size'] = sys.getsizeof(data)
        self.lifespan = meta['lifespan']
        self.length = meta['length']
        self.size = meta['size']
        if header != '':
            h = header
        else:
            h = Tools.serialize(Tools.create_id())
        [self.contents.append(Tools.serialize(x)) for x in (h, meta, pipeline, data)]
        del header
        del meta
        del pipeline
        del data
        
    def load(self, sealed_envelope):
        [self.contents.append(x) for x in sealed_envelope]
        meta = self.get_meta()
        self.lifespan = meta.lifespan
        self.length = meta.length
        self.size = meta.size
        del sealed_envelope
        del meta

    def open(self):
        return [Tools.deserialize(x) for x in self.contents]

    def unpack(self):
        return self.get_raw_header(), self.get_meta(), self.get_pipeline(), self.get_data()

    def seal(self):
        return list(self.contents)

    def get_header(self):
        return self.contents[0]

    def get_raw_header(self):
        return Tools.deserialize(self.contents[0])

    def get_meta(self):
        return Meta(Tools.deserialize(self.contents[1]))

    def get_pipeline(self):
        return Pipeline(Tools.deserialize(self.contents[2]))

    def get_data(self):
        return Tools.deserialize(self.contents[-1])

    def update_data(self, data):
        self.contents.pop()
        self.contents.append(Tools.serialize(data))

    def update_meta(self, meta):
        self.contents.pop(1)
        self.contents.insert(Tools.serialize(meta.extract()), 1)

    def empty(self):
        self.contents.clear()

    def validate(self):
        if len(self.contents) != 4:
            raise Exception('[ENVELOPE] (validation): size missmatch')

class Pipeline(object):
    """
    NAME:           Pipeline

    DESCRIPTION:    A class for storing the envelopes pipeline. Tasks to be 
                    completed, tasks already completed, and task arguments
                    are part of the pipeline object.

    METHODS:        .extract()
                    Returns a dict representation of the pipeline(obj).

                    .load(pipeline)
                    Loads a dict representation of a pipeline(obj) into a
                    pipeline(obj).

                    .consume()
                    Pops the first item in tasks and places it in completed.
                    Returns the popped item.
    """
    def __init__(self, pipeline=None):
        self.kwargs = {}
        self.tasks = collections.deque()
        self.completed = collections.deque()
        if pipeline != None:
            self.load(pipeline)

    def extract(self):
        return {
            'tasks': self.tasks,
            'completed': self.completed,
            'kwargs': self.kwargs
        }

    def load(self, pipeline):
        for k, v in pipeline.items():
            setattr(self, k, v)

    def consume(self):
        current = self.tasks.pop(0)
        self.completed.append(current)
        return current

class Meta(object):
    """
    NAME:           Meta

    DESCRIPTION:    A class for storing the envelopes metadata. Size, length,
                    lifespan, times, and stage, are all part of the meta
                    object.

    METHODS:        .extract()
                    Returns a dict representation of the meta(obj).

                    .load(meta)
                    Loads a dict representation of a meta(obj) into a
                    meta(obj).
    """
    def __init__(self, meta=None):
        self.size = 0
        self.length = 0
        self.lifespan = 0
        self.times = {}
        self.stage = Tools.create_id()
        if meta != None:
            self.load(meta)

    def extract(self):
        return {
            'size': self.size,
            'length': self.length,
            'lifespan': self.lifespan,
            'times': self.times,
            'stage': self.stage
        }

    def load(self, meta):
        for k, v in meta.items():
            setattr(self, k, v)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
