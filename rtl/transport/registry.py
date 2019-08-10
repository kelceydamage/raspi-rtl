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
# Dependancies:
#                   pkgutil
#                   sys
#                   common
#                   transport
#
# Imports
# ------------------------------------------------------------------------ 79->
import pkgutil
import sys

# Globals
# ------------------------------------------------------------------------ 79->
VERSION = '0.5'

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def import_tasks(module_name):
    modules = {}
    try:
        path = next(pkgutil.iter_importers(module_name)).path
    except ImportError as e:
        print('ERROR:', e)
        return modules
    for importer, package_name, _ in pkgutil.iter_modules([path]):
        full_package_name = 'tasks.%s' % (package_name)
        module = importer.find_module(package_name).load_module()
        modules[module.__name__] = module
    return modules

def load_tasks(dirname):
    """
    NAME:           load_tasks

    DESCRIPTION:    Auto loader and parser for task modules. This function is
                    written for efficiency, so I appologize for lack of
                    readability.
    """
    functions = {}
    member_list = []
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = 'tasks.%s' % (package_name)
        module = importer.find_module(package_name).load_module()
        for member in [x for x in dir(module) if 'task_' in x]:
            functions[member] = '{0}.{1}'.format(package_name, member)
    return functions


# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    pass
