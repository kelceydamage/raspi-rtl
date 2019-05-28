#!/usr/bin/env python3
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
# Required Args:        
#
# Optional Args:        
#
# Imports
# ------------------------------------------------------------------------ 79->
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.themes import Theme
from multiprocessing import Queue
from bokeh.palettes import Viridis
from bokeh.palettes import Category10

# Globals
# ------------------------------------------------------------------------ 79->
LOGFILE = 'log/plot.log'
PLOT_QUEUE = Queue()

PLOTS = {
    0: figure(
        plot_width=900, 
        plot_height=300,
        x_axis_type="linear",
        y_axis_type="linear",
        x_minor_ticks=10,
        y_minor_ticks=10
    ),
    1: figure(
        plot_width=900, 
        plot_height=300,
        x_axis_type="linear",
        y_axis_type="linear",
        x_minor_ticks=10,
        y_minor_ticks=10
    ),
    2: figure(
        plot_width=900, 
        plot_height=300,
        x_axis_type="log",
        y_axis_type="log",
        x_minor_ticks=10,
        y_minor_ticks=10,
    )
}
SOURCES = {
    0: {
        'circle': {'x_values': [0], 'y_values': [0], 'color': ['#3333dd']},
        'line': {'x_values': [0], 'y_values': [0], 'color': ['#3333dd']},
        'series': [2]
    },
    1: {
        'circle': {'x_values': [0], 'y_values': [0], 'color': ['#3333dd']},
        'line': {'x_values': [0], 'y_values': [0], 'color': ['#3333dd']},
        'series': [2]
    },
    2: {
        'circle': {'x_values': [0], 'y_values': [0], 'color': ['#3333dd']},
        'line': {'x_values': [0], 'y_values': [0], 'color': ['#3333dd']},
        'line1': {'x_values': [0], 'y_values': [0], 'color': ['#3333dd']},
        'line2': {'x_values': [0], 'y_values': [0], 'color': ['#3333dd']},
        'line3': {'x_values': [0], 'y_values': [0], 'color': ['#3333dd']},
        'line4': {'x_values': [0], 'y_values': [0], 'color': ['#3333dd']},
        'series': [2]
    }
}

COLORMAP = {
    0: 'red', 
    1: 'green', 
    2: 'blue',
    3: 'orange',
    4: 'purple',
    5: 'navy'
}

# Classes
# ------------------------------------------------------------------------ 79->

# Functions
# ------------------------------------------------------------------------ 79->
def log(msg):
    with open(LOGFILE, 'a') as f:
        f.write(str(msg) + '\n')

def draw(sources):
    for i in range(len(sources.keys())):
        if 'series' in sources[i].keys():
            sources[i]['circle']['color'] = [Category10[6][x] for x in sources[i]['series']]
        else:
            sources[i]['circle']['color'] = '#3333dd'
        try:
            PLOTS[i].xaxis.axis_label = sources[i]['x']
            PLOTS[i].yaxis.axis_label = sources[i]['y']
            PLOTS[i].circle(
                x='x_values',
                y='y_values',
                source=ColumnDataSource(data=sources[i]['circle']),
                size=6,
                color='color'
            )
            PLOTS[i].line(
                x='x_values',
                y='y_values',
                source=ColumnDataSource(data=sources[i]['line']),
                color=Category10[6][0],
                line_width=3 # blue
            )
        except Exception as e:
            log('modify_doc: {0}'.format(e))
        if 'line1' in sources[i]:
            try:
                PLOTS[i].line(
                    x='x_values',
                    y='y_values',
                    source=ColumnDataSource(data=sources[i]['line1']),
                    color=Category10[6][1],
                    line_width=3 # yellow
                )
                PLOTS[i].line(
                    x='x_values',
                    y='y_values',
                    source=ColumnDataSource(data=sources[i]['line2']),
                    color=Category10[6][2],
                    line_width=3 # green
                )
                PLOTS[i].line(
                    x='x_values',
                    y='y_values',
                    source=ColumnDataSource(data=sources[i]['line3']),
                    color=Category10[6][3],
                    line_width=3 # red
                )
                PLOTS[i].line(
                    x='x_values',
                    y='y_values',
                    source=ColumnDataSource(data=sources[i]['line4']),
                    color=Category10[6][4],
                    line_width=3 # purple
                )
            except Exception as e:
                log('modify_doc: {0}'.format(e))

def modify_doc(doc):
    draw(SOURCES)

    def update():
        try:
            if not PLOT_QUEUE.empty():
                q_data = PLOT_QUEUE.get()
                if isinstance(q_data, dict):
                    log(q_data.keys())
                    draw(q_data)
        except Exception as e:
            log('callback: {0}'.format(e))

    try:
        doc.add_root(column(PLOTS[0]))
        doc.add_root(column(PLOTS[1]))
        doc.add_root(column(PLOTS[2]))
        doc.add_periodic_callback(update, 20)
    except Exception as e:
        log('tools: {0}'.format(e))