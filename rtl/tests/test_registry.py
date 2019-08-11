"""Test case for registry.py"""
import sys
from rtl.transport.registry import import_tasks
from rtl.transport.registry import load_tasks


def test_registry():
    """Test registry.py"""
    python_path = [
        x for x in sys.path if 'python3' in x and 'site' in x
    ]

    # Test valid module name
    result = import_tasks('rtl.tasks.*')
    assert isinstance(result, dict)

    # Test invalid module name
    result = import_tasks('bob.*')
    assert isinstance(result, dict)

    # Test valid task folder
    result = load_tasks('{0}/rtl/tasks'.format(python_path[0]))
    assert isinstance(result, dict)
