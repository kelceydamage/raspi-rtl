"""Test case for cache.py"""
from rtl.transport.cache import ExperimentalCache


CACHE = ExperimentalCache()


def test_cache_instantiation():
    """Test cache instantiation"""
    cache = ExperimentalCache()
    assert isinstance(cache, ExperimentalCache)


def test_cache_put():
    """Test cache put"""
    result = CACHE.put(b'test', b'10')
    assert result == (b'test', True)


def test_cache_valid_get():
    """Test cache get"""
    result = CACHE.get(b'test')
    assert result == (b'test', b'10')


def test_cache_invalid_get():
    """Test cache get"""
    result = CACHE.get(b'bob')
    assert result == (b'bob', False)


def test_cache_delete():
    """Test cache recore delete"""
    result = CACHE.delete(b'test')
    assert result == (b'test', True)


def test_cache_status():
    """Test cache status"""
    result = CACHE.status()
    assert isinstance(result, dict)


def test_cache_info():
    """Test cache info"""
    result = CACHE.info()
    assert isinstance(result, dict)


def test_cache_sync():
    """Test cache synce"""
    result = CACHE.sync()
    assert result is None
