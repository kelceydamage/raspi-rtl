"""Test case for cache.py"""
from rtl.transport.cache import ExperimentalCache


def test_cache():
    """Test cache.py"""
    # Test cache instantiation
    cache = ExperimentalCache()
    assert isinstance(cache, ExperimentalCache)

    # Test cache put
    result = cache.put(b'test', b'10')
    assert result == (b'test', True)

    # Test cache get
    result = cache.get(b'test')
    assert result == (b'test', b'10')

    # Test cache get
    result = cache.get(b'bob')
    assert result == (b'bob', False)

    # Test cache recore delete
    result = cache.delete(b'test')
    assert result == (b'test', True)

    # Test cache status
    result = cache.status()
    assert isinstance(result, dict)

    # Test cache info
    result = cache.info()
    assert isinstance(result, dict)

    # Test cache recore delete
    result = cache.sync()
    assert result is None

    # Test cache recore delete
    # r = cache.drop()
    # print(r)
    # assert r == (b'test', True)
