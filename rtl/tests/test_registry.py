from rtl.transport.registry import import_tasks
from rtl.transport.registry import load_tasks
import sys

def test_registry():
    pythonPath = [
        x for x in sys.path if 'python3' in x and 'site' in x
    ]

    # Test valid module name
    r = import_tasks('rtl.tasks.*')
    assert isinstance(r, dict)

    # Test invalid module name
    r = import_tasks('bob.*')
    assert isinstance(r, dict)

    # Test valid task folder
    r = load_tasks('{0}/rtl/tasks'.format(pythonPath[0]))
    assert isinstance(r, dict)