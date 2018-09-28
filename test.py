import numpy as np
import time
import math


def test0():
    # option 0
    l1 = []
    l2 = []
    d1 = {}
    seed = [[1.0, 2.0, 3.0] for x in range(loop)]
    t = time.perf_counter()
    length = loop
    size = chunk
    if length <= 1 or length == size:
        print('opt 1')
        time.sleep(0.001)
    else:
        l2 = seed
        seed = []
        for i in range(len(l2)):
            l1.append(l2.pop())
            if i % chunk == 0:
                seed = l1
                l1 = []
                time.sleep(send)
        time.sleep(state)

    t2 = time.perf_counter() - t
    return t2


def test1():
    # option 1
    l1 = []
    l2 = []
    d1 = {}
    seed = [[1.0, 2.0, 3.0] for x in range(loop)]
    t = time.perf_counter()
    length = loop
    size = chunk
    if length <= 1 or length == size:
        print('opt 1')
        time.sleep(0.001)
    else:
        l2 = seed
        seed = []
        while l2:
            l1.append(l2.pop())
            if len(l1) % chunk == 0:
                seed = l1
                l1 = []
                time.sleep(send)
        time.sleep(state)

    t2 = time.perf_counter() - t
    return t2


def test2():
    # option 2
    l1 = []
    l2 = []
    d1 = {}
    seed = [[1.0, 2.0, 3.0] for x in range(loop)]
    t = time.perf_counter()
    length = loop
    size = chunk
    if length <= 1 or length == size:
        print('opt 1')
        time.sleep(0.001)
    else:
        l2 = seed
        seed = []
        for i in range(len(l2)):
            if i % chunk == 0:
                seed = l2[:chunk]
                del l2[:chunk]
                time.sleep(send)
        time.sleep(state)

    t2 = time.perf_counter() - t
    return t2


def test3():
    # option 3
    l1 = []
    l2 = []
    d1 = {}
    seed = [[1.0, 2.0, 3.0] for x in range(loop)]
    t = time.perf_counter()
    length = loop
    size = chunk
    if length <= 1 or length == size:
        print('opt 1')
        time.sleep(0.001)
    else:
        for i in range(len(seed)):
            if i % chunk == 0:
                d1[i] = seed[:chunk]
                del seed[:chunk]
            
        for k, v in d1.items():
            seed = v
            time.sleep(send)
        del d1
        time.sleep(state)
    t2 = time.perf_counter() - t
    return t2


def test4():
    print('RUN test4')
    # option 4
    l1 = []
    l2 = []
    d1 = {}
    _len = len
    seed = [[1.0, 2.0, 3.0] for x in range(loop)]
    size = len(seed)
    ck = chunk
    t = time.perf_counter()
    if size <= 1 or size == ck:
        print('opt 1')
        time.sleep(0.001)
    else:
        for i in range(size):
            if i % ck == 0:
                d1[i] = seed[:ck]
                del seed[:ck]
            
        k = list(d1.items())
        #print(d1.keys())
        for i in range(_len(k)):
            seed = k.pop()[1]
            #time.sleep(send)
            #print('...')
        #time.sleep(state)
            
        t2 = time.perf_counter() - t
        return t2


def test6():
    print('RUN test6')
    # option 4
    l1 = []
    l2 = []
    d1 = {}
    seed = [[1.0, 2.0, 3.0] for x in range(loop)]
    size = len(seed)
    start = 0
    groups = math.ceil(size / chunk)
    ck = chunk

    t = time.perf_counter()
    l1 = seed
    if size <= 1 or size == ck:
        time.sleep(0.001)
    else:
        for i in range(groups):
            d1[i] = l1[start:start + ck]
            seed = d1[i]
            start += ck
            
        t2 = time.perf_counter() - t
        return t2

def test5():
    print('RUN test5')
    # option 4
    l1 = []
    l2 = []
    d1 = {}
    seed = [[1.0, 2.0, 3.0] for x in range(loop)]
    size = len(seed)
    start = 0
    groups = math.ceil(size / chunk)
    ck = chunk
    l1 = seed
    t = time.perf_counter()
    
    if size <= 1 or size == ck:
        time.sleep(0.001)
    else:
        for i in range(groups):
            d1[i] = l1[start:start + ck]
            #seed = d1[i]
            start += ck
            
        t2 = time.perf_counter() - t
        return t2

def test7():
    # option 2
    l1 = []
    l2 = []
    d1 = {}
    seed = [[1.0, 2.0, 3.0] for x in range(loop)]
    t = time.perf_counter()
    length = loop
    size = chunk
    l2 = []
    start = 0
    if length <= 1 or length == size:
        print('opt 1')
        time.sleep(0.001)
    else:
        l2 = np.array_split(np.array(seed), length / size)
        seed.clear()
        while l2:
            seed = l2.pop().tolist()

            #time.sleep(send)
            start += size
            print('...')
        #time.sleep(state)

    t2 = time.perf_counter() - t
    return t2



'''
cdef void chunk(self) except *:
    t = time.perf_counter()
    cdef uint_fast16_t length
    cdef uint_fast16_t chunk_size = <uint_fast16_t>CHUNKING_SIZE
    cdef list data
    cdef uint_fast16_t start = 0
    #cdef long loops
    #length = (<uint_fast16_t>self.envelope.get_length())
    #print('LEN', length)
    if self.envelope.get_length() <= 1 or self.envelope.get_length() == chunk_size:
        self.send()
    else:
        #loops = math.ceil(self.envelope.get_length() / CHUNKING_SIZE) 
        data = np.array_split(np.array(self.envelope.data), 10)
        self.envelope.data.clear()
        while data:
            self.envelope.data = data.pop().tolist()
            self.create_state(self.envelope.get_header(), self.envelope.get_length())
            self.send()
            start += chunk_size
            print('R sendbuff', time.perf_counter() - t)
            t = time.perf_counter()
'''


tests = 8
times = {}
for i in range(tests):
    times[i] = []
loop = 50000
chunk =  5000
state = 0.001
send = 0.007


for i in range(10):
    for n in range(5,7):
        times[n].append(eval('test{0}'.format(n))())
        time.sleep(1)

for k, v in times.items():
    if len(v) != 0:
        print('{0}: avg {1:.8f}s'.format(k, sum(v) / len(v)))
        print('{0}: min {1:.8f}s'.format(k, min(v)))
        print('{0}: max {1:.8f}s'.format(k, max(v)))
        print('-'*79)

seed = [[1.0, 2.0, 3.0] for x in range(loop)]
d1 = {}
t = time.perf_counter()

d1[0] = seed[:chunk]


t2 = time.perf_counter() - t
print('{0:.8f}s'.format(t2))

seed = [[1.0, 2.0, 3.0] for x in range(loop)]
d1 = {}
l1 = []
t = time.perf_counter()
l1 = seed
d1[0] = l1[:chunk]
t2 = time.perf_counter() - t
print('{0:.8f}s'.format(t2))










