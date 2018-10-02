#! /usr/bin/env python3

from distutils.core import setup
from distutils.extension import Extension
import platform
import numpy
import zmq

USE_CYTHON = True

ext = '.pyx' if USE_CYTHON else '.c'

extentions = [
    Extension(
        "common.datatypes",
        sources=["common/datatypes{0}".format(ext)],
        extra_compile_args=['-std=c++11'],
        language="c++"
        ),
    Extension(
        "common.encoding",
        sources=["common/encoding{0}".format(ext)],
        extra_compile_args=['-std=c++11'],
        language="c++"
        ),
    Extension(
        "common.print_helpers",
        sources=["common/print_helpers{0}".format(ext)],
        extra_compile_args=['-std=c++11'],
        language="c++"
        ),
    Extension(
        "transport.relay",
        sources=["transport/relay{0}".format(ext)],
        extra_compile_args=['-std=c++11'],
        language="c++"
        ),
    Extension(
        "transport.node",
        sources=["transport/node{0}".format(ext)],
        extra_compile_args=['-std=c++11'],
        language="c++"
        ),
    Extension(
        "transport.dispatch",
        sources=["transport/dispatch{0}".format(ext)],
        extra_compile_args=['-std=c++11'],
        language="c++"
        ),
    ]

if USE_CYTHON:
    from Cython.Build import cythonize
    import Cython
    Cython.Compiler.Options.annotate = True
    Cython.Compiler.Options.warning_errors = True
    Cython.Compiler.Options.convert_range = True
    Cython.Compiler.Options.cache_builtins = True
    Cython.Compiler.Options.gcc_branch_hints = True
    Cython.Compiler.Options.embed = False
    extentions = cythonize(extentions)

setup(
    ext_modules = extentions,
    include_dirs=[numpy.get_include(), zmq.get_includes()]
)