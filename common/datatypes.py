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
#                   cache
#                   encoding
#
# Imports
# ------------------------------------------------------------------------ 79->
from transport.cache import Cache
from common.encoding import Tools

# Globals
# ------------------------------------------------------------------------ 79->
VERSION = '0.3'


# Classes
# ------------------------------------------------------------------------ 79->

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
    NAME:           Envelope v0.3

    DESCRIPTION:    A class of utility functions used by the datatypes. It
                    stores a header, meta, pipeline, and data, for sending
                    between members of the transport framework.

    METHODS:        ._compression()
                    Check for compression flag or return False.

                    ._flatten(obj)
                    If compressed then uncompress.

                    ._compress(obj)
                    If not compressed then compress.

                    ._set_params()
                    Assign specific instance attributes from meta.

                    ._complete_meta
                    Assing specific meta attributes packed content.

                    .open(compressed=False)
                    Returns the envelope(obj) in it's completely uncompressed
                    form. If compressed is True, return the contents without
                    decompressing them.

                    .seal()
                    Returns the content as a list of bytes objects for
                    transmission.

                    .cache_data()
                    Cache the data content.

                    .retrieve_cache()
                    Retrieve cached data content.

                    .check_for_cached_data()
                    Check to see if data content is cached.

                    .pack(header, meta, pipeline, data)
                    Packs up a header, meta, pipeline, and data
                    into and envelope(obj).

                    .load(sealed_envelope)
                    Loads a compressed envelope right off the wire into an
                    envelope object.

                    .get_length()
                    Returns the envelopes length in either raw or compressed
                    form based on the self.compressed flag.

                    .get_lifespan()
                    Returns the envelopes lifespan in either raw or compressed
                    form based on the self.compressed flag.

                    .get_header()
                    Returns the envelopes header in either raw or compressed
                    form based on the self.compressed flag.

                    .get_meta()
                    Returns the envelopes meta in either raw or compressed
                    form based on the self.compressed flag.

                    .get_pipeline()
                    Returns the envelopes pipeline in either raw or compressed
                    form based on the self.compressed flag.

                    .get_data()
                    Returns the envelopes data in either raw or compressed
                    form based on the self.compressed flag.

                    .validate()
                    Inactive.
    """
    __slots__ = [
        'header',
        'meta',
        'pipeline',
        'data',
        'manifest',
        'cached',
        'compressed',
        'cache',
        'length',
        'lifespan'
        ]

    def __init__(self, cached=False):
        self.compressed = False
        self.cached = cached
        self.manifest = ['header', 'meta', 'pipeline', 'data']
        self.cache = Cache()

    def __getattr__(self, key):
        if self._compression() and key in self.manifest:
            return self._compress(object.__getattribute__(self, key))
        else:
            return self._flatten(object.__getattribute__(self, key))

    def __setattr__(self, key, value):
        if self._compression() and key in self.manifest:
            object.__setattr__(self, key, self._compress(value))
        else:
            object.__setattr__(self, key, self._flatten(value))

    def __len__(self):
        return self.length

    def __getitem__(self, key):
        if key not in self.__slots__:
            return self.__missing__(key)
        return self.__getattr__(key)

    def __missing__(self, key):
        return False

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        pass

    def __contains__(self, key):
        if key in self.__slots__:
            return True
        return False

    def _compression(self):
        try:
            return object.__getattribute__(self, 'compressed')
        except AttributeError:
            return False

    def _flatten(self, obj):
        if not isinstance(obj, bytes):
            return obj
        return Tools.deserialize(obj)

    def _compress(self, obj):
        if isinstance(obj, bytes):
            return obj
        elif isinstance(obj, Cache):
            return obj
        else:
            return Tools.serialize(obj)

    def _set_params(self):
        meta = self.get_meta()
        self.length = meta['length']
        self.lifespan = meta['lifespan']

    def _complete_meta(self):
        self.meta['lifespan'] = len(self.pipeline['tasks'])
        self.meta['length'] = len(self.data)
        self._set_params()

    def open(self, compressed=False):
        self.compressed = compressed
        return [self[k] for k in self.manifest]

    def seal(self):
        self.compressed = True
        if self.cached:
            self.cache_data()
        return self.open(True)

    def cache_data(self):
        key = Tools.create_key(Tools.create_id())
        r = self.cache.put(key, self['data'])
        if r[1]:
            self['meta']['cache_key'] = key
            self['data'].clear()

    def retrieve_cache(self):
        key = self['meta']['cache_key']
        r = self.cache.get(key)
        self.update_data(r[1])
        self['meta']['spent_key'] = key
        self['meta']['cache_key'] = None

    def check_for_cached_data(self):
        if self['meta']['cache_key'] is not None:
            self.retrieve_cache()

    def pack(self, header, meta, pipeline, data):
        self.compressed = False
        if header == '':
            header = Tools.create_id()
        self.__setattr__('header', header)
        self.__setattr__('meta', meta)
        self.check_for_cached_data()
        self.__setattr__('pipeline', pipeline)
        self.__setattr__('data', data)
        self._complete_meta()
        del header
        del meta
        del pipeline
        del data

    def load(self, sealed_envelope):
        self.compressed = True
        self.pack(
            sealed_envelope[0],
            sealed_envelope[1],
            sealed_envelope[2],
            sealed_envelope[3]
        )
        self._set_params()
        del sealed_envelope

    def get_length(self):
        return self._flatten(self.length)

    def get_lifespan(self):
        return self._flatten(self.lifespan)

    def get_header(self):
        return self._flatten(self.header)

    def get_meta(self):
        return self._flatten(self.meta)

    def get_pipeline(self):
        return self._flatten(self.pipeline)

    def get_data(self):
        return self._flatten(self.data)

    def validate(self):
        pass


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
        self.tasks = []
        self.completed = []
        if pipeline is not None:
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
        self.length = 0
        self.lifespan = 0
        self.times = {}
        self.stage = Tools.create_id()
        self.cache_key = None
        self.spent_key = None
        if meta is not None:
            self.load(meta)

    def extract(self):
        return {
            'length': self.length,
            'lifespan': self.lifespan,
            'times': self.times,
            'stage': self.stage,
            'cache_key': self.cache_key,
            'spent_key': self.spent_key
        }

    def load(self, meta):
        for k, v in meta.items():
            setattr(self, k, v)

# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
