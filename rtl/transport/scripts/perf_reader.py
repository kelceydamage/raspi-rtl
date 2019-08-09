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
#

# Imports
# ------------------------------------------------------------------------ 79->
import os
import ast
import statistics
os.sys.path.append('{0}{1}'.format(os.getcwd().split('rtl')[0], 'rtl'))
from common.print_helpers import timer
from common.print_helpers import Logger
from common.print_helpers import padding


# Globals
# ------------------------------------------------------------------------ 79->
LOG_PATH = 'var/log/'
FILENAME = 'performance.log'
CURR_DIR = os.getcwd()
LOG = Logger(3)
PROFILE = False

# Classes
# ------------------------------------------------------------------------ 79->


class PerfReader(object):
    def __init__(self):
        self.file = '{0}/{1}{2}'.format(get_root_dir(), LOG_PATH, FILENAME)
        self.map = {}

    @timer(LOG, 'perfreader', PROFILE)
    def read(self):
        self.open()
        self.calculate()
        self.display()

    @timer(LOG, 'perfreader', PROFILE)
    def open(self):
        print(self.file)
        with open(self.file, 'r') as f:
            line = f.readline()
            while line:
                self.aggregate_lines(ast.literal_eval(line))
                line = f.readline()

    @timer(LOG, 'perfreader', PROFILE)
    def open_all(self):
        with open(self.file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            self.aggregate_lines(ast.literal_eval(line))

    @timer(LOG, 'perfreader', PROFILE)
    def t_open(self):
        with open(self.file, 'r') as f:
            line = f.readline()
            self.aggregate_lines(ast.literal_eval(line))

    @timer(LOG, 'perfreader', PROFILE)
    def aggregate_lines(self, _dict):
        self.populate(_dict)
        cursor = self.map[_dict['system']][_dict['name']]
        cursor['count'] += 1
        cursor['sum'] += float(_dict['perf_time'])
        cursor['times'].append(float(_dict['perf_time']))
        self.map[_dict['system']][_dict['name']] = cursor
        del cursor

    @timer(LOG, 'perfreader', PROFILE)
    def populate(self, _dict):
        if _dict['system'] not in self.map.keys():
            self.map[_dict['system']] = {}
        if _dict['name'] not in self.map[_dict['system']].keys():
            self.map[_dict['system']][_dict['name']] = {
                'count': 0,
                'times': [],
                'min': 0,
                'max': 0,
                'mean': 0,
                'stddev': 0,
                'per1000': 0,
                'sum': 0
            }

    @timer(LOG, 'perfreader', PROFILE)
    def stats(self, call):
        call['min'] = '{:4.8f}'.format(min(call['times']))
        call['max'] = '{:4.8f}'.format(max(call['times']))
        if call['count'] > 1:
            call['mean'] = '{:4.8f}'.format(statistics.mean(call['times']))
            call['stddev'] = '{:4.8f}'.format(statistics.stdev(call['times']))
        call['per1000'] = '{:4.8f}'.format(
            call['sum'] / (call['count'] / 1000)
            )
        call['times'] = []
        return call

    @timer(LOG, 'perfreader', PROFILE)
    def calculate(self):
        for system in self.map.keys():
            for method in self.map[system].keys():
                cursor = self.map[system][method]
                self.map[system][method] = self.stats(cursor)

    def print_ranked_header(self):
        print('{0}{1}{2}{3}'.format(
            padding('Class', 32),
            padding('Method', 32),
            padding('per 1000 calls', 26),
            'count'
            ))

    @timer(LOG, 'perfreader', PROFILE)
    def display(self):
        ranked = []
        for system in self.map.keys():
            # print('SYSTEM: {0}'.format(system))
            for method in self.map[system].keys():
                # print('\t * METHOD: {0}'.format(method))
                # for k, v in self.map[system][method].items():
                #    print('\t\t - {0}: {1}'.format(k, v))
                ranked.append([
                    system,
                    method,
                    self.map[system][method]['per1000'],
                    self.map[system][method]['count']
                    ])
        ranked.sort(key=lambda x: float(x[2]), reverse=True)
        print()
        print('RANKED')
        print()
        self.print_ranked_header()
        print('-' * 100)
        for item in ranked:
            print('{0}{1}{2}{3}'.format(
                padding('[{0}]'.format(item[0]), 32),
                padding('* {0}()'.format(item[1]), 32),
                padding('{0} s'.format(item[2]), 26),
                item[3]
                ))


# Functions
# ------------------------------------------------------------------------ 79->


@timer(LOG, 'get_root_dir', PROFILE)
def get_root_dir():
    path_components = CURR_DIR.split('/')
    document_root_components = []
    while path_components:
        component = path_components.pop(0)
        document_root_components.append(component)
        if component == 'rtl':
            root = '/'.join(document_root_components)
            break
    return root


# Main
# ------------------------------------------------------------------------ 79->
if __name__ == '__main__':
    PR = PerfReader()
    PR.read()
    # PR.open_all()
    # print(PR.map)
