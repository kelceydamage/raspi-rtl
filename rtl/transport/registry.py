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
Dependancies:
    pkgutil

"""
# Imports
# ------------------------------------------------------------------------ 79->
import pkgutil


# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def loader(path):
    """
    NAME:           load_tasks

    DESCRIPTION:    Auto loader and parser for task modules. This function is
                    written for efficiency, so I appologize for lack of
                    readability.
    """
    modules = {}
    for importer, package_ame, _ in pkgutil.iter_modules([path]):
        module = importer.find_module(package_ame).load_module()
        modules[module.__name__] = module
    return modules


def import_tasks(module_name):
    """Locate the path to the module for importing"""
    if '/' in module_name:
        return loader(module_name)
    try:
        path = next(pkgutil.iter_importers(module_name)).path
    except ImportError as error:
        print('ERROR:', error)
        return {}
    return loader(path)


# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':  # pragma: no cover
    print(import_tasks('rtl.tasks.*'))
