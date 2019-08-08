#! /usr/bin/env python3

from distutils.core import setup
from distutils.extension import Extension
from os.path import dirname
import platform
import numpy
import zmq

c_options = { 
    'gpu': False,
}

if 'tegra' in platform.release():
    c_options['gpu'] = True

print('Generate config.pxi')
with open('config.pxi', 'w') as fd:
    for k, v in c_options.items():
        fd.write('DEF %s = %d\n' % (k.upper(), int(v)))

USE_CYTHON = True

ext = '.pyx' if USE_CYTHON else '.c'

PYX_FILES = [
    "common.datatypes",
    "common.encoding",
    "common.print_helpers",
    "common.normalization",
    "common.regression",
    "common.transform",
    "common.task",
    "transport.relay",
    "transport.node",
    "transport.dispatch",
    "tasks.open_array",
    "tasks.normalize"
]

extensions = []
for i in PYX_FILES:
    extensions.append(
        Extension(
            i,
            sources=['{0}{1}'.format(i.replace('.', '/'), ext)],
            extra_compile_args=['-std=c++11'],
            language="c++"
            )
        )

if USE_CYTHON:
    from Cython.Build import cythonize
    import Cython
    Cython.Compiler.Options.annotate = True
    Cython.Compiler.Options.warning_errors = True
    Cython.Compiler.Options.convert_range = True
    Cython.Compiler.Options.cache_builtins = True
    Cython.Compiler.Options.gcc_branch_hints = True
    Cython.Compiler.Options.embed = False
    extensions = cythonize(extensions)

setup(
    name='RTL',
    version='3-experimental',
    description='Raspi Transport Layer',
    author='Kelcey Jamison-Damage',
    author_email='',
    url='https://github.com/kelceydamage/rtl.git'
    ext_modules = extensions,
    include_dirs = [numpy.get_include(), zmq.get_includes()]
)
