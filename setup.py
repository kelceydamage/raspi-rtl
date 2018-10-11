#! /usr/bin/env python3

from distutils.core import setup
from distutils.extension import Extension
import platform
import numpy
import zmq

USE_CYTHON = True

ext = '.pyx' if USE_CYTHON else '.c'

PYX_FILES = [
    "common.datatypes",
    "common.encoding",
    "common.print_helpers",
    "transport.relay",
    "transport.node",
    "transport.dispatch"
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
    ext_modules = extensions,
    include_dirs = [numpy.get_include(), zmq.get_includes()]
)
