"""Test case for registry.py"""
from rtl.transport.registry import import_tasks


def test_registry():
    """Test registry.py"""

    # Test valid module name
    result = import_tasks('rtl.tasks.*')
    assert isinstance(result, dict)

    # Test invalid module name
    result = import_tasks('bob.*')
    assert isinstance(result, dict)

    # Test module path
    result = import_tasks('rtl/tasks')
    assert isinstance(result, dict)
