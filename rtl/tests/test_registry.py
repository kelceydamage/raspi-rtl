"""Test case for registry.py"""
from rtl.transport.registry import import_tasks


def test_registry_valid_module():
    """Test valid module name"""
    result = import_tasks('rtl.tasks.*')
    assert isinstance(result, dict)


def test_registry_invalid_module():
    """Test invalid module name"""
    result = import_tasks('bob.*')
    assert isinstance(result, dict)


def test_registry_valid_path():
    """Test module path"""
    result = import_tasks('rtl/tasks')
    assert isinstance(result, dict)
