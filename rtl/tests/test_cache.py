from rtl.transport.cache import ExperimentalCache
import sys

def test_cache():
    # Test cache instantiation
    cache = ExperimentalCache()
    assert isinstance(cache, ExperimentalCache)

    # Test cache put
    r = cache.put(b'test', b'10')
    assert r == (b'test', True)

    # Test cache get
    r = cache.get(b'test')
    assert r == (b'test', b'10')

    # Test cache get
    r = cache.get(b'bob')
    assert r == (b'bob', False)

    # Test cache recore delete
    r = cache.delete(b'test')
    assert r == (b'test', True)

    # Test cache status
    r = cache.status()
    assert isinstance(r, dict)

    # Test cache info
    r = cache.info()
    assert isinstance(r, dict)

    # Test cache recore delete
    r = cache.sync()
    assert r == None

    # Test cache recore delete
    # r = cache.drop()
    # print(r)
    # assert r == (b'test', True)

    