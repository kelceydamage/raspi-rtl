#!python
#cython: language_level=3, cdivision=True
###boundscheck=False, wraparound=False //(Disabled by default)
# ------------------------------------------------------------------------ 79->
# Author: Kelcey Damage
# Cython: 0.28+
# Doc
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
from transport.cache import Cache  # pragma: no cover

from common.encoding cimport Tools
import time
import ctypes
cimport cython
from libcpp.list cimport list as cpplist
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.list cimport list as clist
from libcpp.utility cimport pair
from libcpp.string cimport string
#from libcpp.map cimport map as cmap
from libcpp.unordered_map cimport unordered_map
from libc.stdint cimport uint_fast8_t, uint_fast16_t
from libc.stdint cimport int_fast16_t
from libc.stdio cimport printf, sprintf
from libc.stdlib cimport atoi
from posix cimport time as p_time
from libcpp.typeinfo cimport type_info
import struct as pystruct
import cbor
#import numpy as np
import numpy as np
cimport numpy as np
import io

#import tensorflow as tf

from cpython.bytes cimport PyBytes_FromStringAndSize


# Globals
# ------------------------------------------------------------------------ 79->

TOOLS = Tools()

# Classes
# ------------------------------------------------------------------------ 79->

cdef class Parcel(object):
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
        self.contents = []
        self.lifespan = 0

    cpdef pack(self, route, envelope):
        self.contents.append(route)
        self.contents.append(b'')
        self.contents.extend(envelope.seal())

    cpdef unpack(self):
        envelope = Envelope()
        envelope.load(list(self.contents)[2:])
        return self.contents[0], envelope

    cpdef load(self, parcel):
        envelope = Envelope()
        envelope.load(parcel[2:])
        self.pack(parcel[0], envelope)

    cpdef seal(self):
        return list(self.contents)


cdef class Container:
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
        'lifespan',
        'tools'
        ]

    def __init__(self, bint cached=False):
        self.manifest = [b'header', b'meta', b'pipeline', b'data']

    def __cinit__(self, bint cached=False):
        self.manifest = [b'header', b'meta', b'pipeline', b'data']

    '''
    def __getattr__(self, str key):
        if self._compression() and self._has(self.manifest, key.encode()):
            return self._compress(object.__getattribute__(self, key))
        else:
            return self._flatten(object.__getattribute__(self, key))

    cdef int_fast16_t _set(self, char[] key, string value) except -1:
        if self._compression() and self._has(self.manifest, <string>key):
            setattr(self, bytes(key).decode(), self._compress(value))
            return 0
        return -1

    def __len__(self):
        return self.length

    def __getitem__(self, str key):
        if key not in self.__slots__:
            return self.__missing__(key)
        return self.__getattr__(key)

    def __missing__(self, str key):
        return False

    def __setitem__(self, str key, object value):
        self.__setattr__(key, value)

    def __delitem__(self, str key):
        pass

    def __contains__(self, str key):
        if key in self.__slots__:
            return True
        return False

    cdef bint _has(self, vector[string] v, string key):
        cdef long i
        cdef long l = v.size()
        for i in range(l):
            if v[i] == key:
                return True
        return False

    cdef bint _compression(Container self):
        try:
            return object.__getattribute__(self, 'compressed')
        except AttributeError:
            return False

    cdef object _flatten(Container self, object obj):
        if not isinstance(obj, bytes):
            return obj
        return TOOLS.deserialize(obj)

    cdef object _compress(Container self, object obj):
        if isinstance(obj, bytes):
            return obj
        elif isinstance(obj, Cache):
            return obj
        else:
            return TOOLS.serialize(obj)
    '''


cdef class Envelope:
    """
    NAME:           Envelope v0.3

    DESCRIPTION:    A class of utility functions used by the datatypes. It
                    stores a header, meta, pipeline, and data, for sending
                    between members of the transport framework.

    METHODS:        ._set_params()
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
        'lifespan',
        'tools'
        ]

    def __init__(self, bint cached=False):
        #super(Envelope, self).__init__(cached=False)
        self.manifest = [b'header', b'meta', b'pipeline', b'data']

    def __cinit__(self, bint cached=False):
        #super(Envelope, self).__init__(cached=False)
        self.manifest = [b'header', b'meta', b'pipeline', b'data']

    cpdef list open(self, bint compressed=False):
        cdef long i
        cdef list l = []
        for i in range(self.get_length()):
            l.append(np.frombuffer(self.data[i]))
        return l

    cpdef void pack(self, dict meta, list data):
        #t = time.perf_counter()
        cdef string _id = TOOLS.create_id()
        cdef np.ndarray h = np.ndarray(
            (1,), dtype=[('id', 'a70'), ('lifespan', 'i4'), ('length', 'i4'), ('shape', 'i4')]
            )
        self.header = h
        self.header['id'] = _id
        self.header['lifespan'] = <int>len(meta['tasks'])
        self.header['length'] = <int>len(data)
        self.header['shape'] = len(data[0])
        self.meta = meta
        self.data = np.ndarray(
            (self.header['length'][0], (self.header['shape'][0])), buffer=np.array(data), dtype=float
            ).tobytes()
        self.unseal = True
        #print('pack {0:.8f}'.format(time.perf_counter() - t))

    cdef void load(self, list sealed_envelope, bint unseal=False):
        #t = time.perf_counter()
        self.unseal = unseal
        self.header = np.frombuffer(
            sealed_envelope[0],
            dtype=[
                ('id', 'a70'), 
                ('lifespan', 'i4'), 
                ('length', 'i4'),
                ('shape', 'i4')
                ]
            ).reshape(1, )
        self.header.setflags(write=1)
        self.data = sealed_envelope[2]
        if self.unseal:
            self.meta = cbor.loads(sealed_envelope[1])
        else:
            self.sealed_meta = sealed_envelope[1]
        #print('E load {0:.8f}'.format(time.perf_counter() - t))

    cdef list seal(self):
        #t = time.perf_counter()
        #self.update_header()
        cdef: 
            string m = <string>cbor.dumps(self.meta)
            string h = <string>self.header.tobytes()
            list l = []
        if self.unseal:
            l = [h, m, self.data]
            #print(l)
            #print('E seal T {0:.8f}'.format(time.perf_counter() - t))
            return l
        l = [self.header.tobytes(), self.sealed_meta, self.data]
        #print(l)
        #print('E seal F {0:.8f}'.format(time.perf_counter() - t))
        return l

    cdef void update_header(self):
        self.header['length'][0] = len(self.data)

    cdef void consume(self):
        self.meta['completed'].append(self.meta['tasks'].pop(0))
        self.header['lifespan'][0] -= 1

    cdef long get_shape(self):
        return self.header['shape'][0]

    cdef long get_lifespan(self):
        return self.header['lifespan'][0]

    cdef long get_length(self):
        return self.header['length'][0]

    cdef string get_header(self):
        return self.header['id'][0]
    
    cdef string get_sealed_data(self):
        return self.data

    cpdef np.ndarray result(self):
        return self.get_data()

    cdef np.ndarray get_data(self):
        #print(self.get_length())
        return np.frombuffer(self.data, dtype=float).reshape(self.get_length(), self.get_shape())

    cdef void set_data(self, np.ndarray data):
        self.header['length'] = len(data)
        self.header['shape'] = len(data[0])
        self.data = data.tobytes()

# Functions
# ------------------------------------------------------------------------ 79->

cdef Pipeline map_to_pipeline(dict _dict):
    cdef Pipeline p
    p.tasks = <clist[string]>(_dict['tasks'])
    return p

cdef np.ndarray map_to_meta(dict _dict):
    cdef list datatypes = [(x[0].decode(), 'a8') for x in list(_dict.items())]
    cdef np.ndarray m = np.fromiter(
        _dict.items(),
        dtype=datatypes,
        count=len(_dict)
        )
    return m

cdef Data map_to_data(list _list):
    cdef Data d
    cdef Segment s
    cdef long i
    cdef long l = len(_list)
    for i in range(l):
        s = <Segment>_list[i]
        d.push_back(s)
    return d

cdef string version():
    cdef string version = b'0.4'
    return version

cdef np.ndarray init_meta():
    cdef np.ndarray m = np.ndarray([(0, 0)],
        dtype=[('lifespan', 'i4'), ('length', 'i16')]
        )
    return m

cdef Pipeline init_pipeline():
    cdef Pipeline p
    p.tasks = []
    p.completed = []
    p.kwargs[b'version'] = string(VERSION)
    return p

cdef Data init_data():
    cdef Data d
    return d

cdef list get_datatypes(dict _dict):
    return [(x[0], 'a32') for x in list(_dict.items())]

cpdef np.ndarray dataFrame(object obj, tuple shape, object dtype):
    t1 = time.time()
    cdef np.ndarray a
    if isinstance(obj, dict):
        a = map_to_ndarray(obj, dtype)
    else:
        a = list_to_ndarray(obj, dtype, shape)
    print('DF C++\t\t {0:.8f}'.format(time.time() - t1))
    return a

cdef np.ndarray list_to_ndarray(list obj, type dtype, tuple shape):
    t1 = time.time()
    cdef np.ndarray a = np.ndarray(shape, buffer=np.array(obj), dtype=dtype)
    print('LtoA C++\t {0:.8f}'.format(time.time() - t1))
    return a

cdef np.ndarray map_to_ndarray(dict obj, list dtype):
    #cdef list datatypes = [(x[0].decode(), 'a8') for x in list(_dict.items())]
    t1 = time.time()
    cdef np.ndarray m = np.fromiter(obj.items(), dtype=dtype)
    print('DtoA C++\t {0:.8f}'.format(time.time() - t1))
    return m

cpdef list dataFrame3(list l1, dict d1):
    t1 = time.time()
    cdef np.ndarray s1x = map_to_meta(d1)
    cdef np.ndarray s2x = np.ndarray((len(l1), len(l1[0])), buffer=np.array(l1), dtype=float)
    cdef list c1 = [(s1x.tobytes(), s2x.tobytes())]
    print('D3b C++\t\t {0:.8f}'.format(time.time() - t1))
    return c1

# Main
# ------------------------------------------------------------------------ 79->
