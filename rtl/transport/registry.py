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
"""
Thhis module provides dynamically loads tasks as provided in the raspi-tasks
package.

Note:
    This is not intented to be used for any other reason. Standard python \
        standard python importing should always be used.

"""


# Imports
# ------------------------------------------------------------------------ 79->
import pkgutil


# Functions
# ------------------------------------------------------------------------ 79->
def _loader(path):
    """Load all modules located within the given path. Add each loaded
    module to a dict of modules.

    Warning:
        This is a private function and should never be called directly.

    Args:
        path (str): path to a folder containing modules.

    Returns:
        dict: a map of names and module references.

    """
    modules = {}
    for importer, package_ame, _ in pkgutil.iter_modules([path]):
        module = importer.find_module(package_ame).load_module()
        modules[module.__name__] = module
    return modules


def import_tasks(module_name):
    """Convert module name into a path and call loader on the path.

    Example:
        .. code-block:: Python

            modules = import_tasks('rtl.tasks.*')

    Args:
        module_name (str): either a path or a name referencing a valid module.

    Returns:
        dict: a map of names and module references.

    """
    if '/' in module_name:
        return _loader(module_name)
    try:
        path = next(pkgutil.iter_importers(module_name)).path
    except ImportError as error:
        print('ERROR:', error)
        return {}
    return _loader(path)


# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':  # pragma: no cover
    print(import_tasks('rtl.tasks.*'))
