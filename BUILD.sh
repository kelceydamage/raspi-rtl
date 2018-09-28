# precompile c++ modules
cython -a --cplus common/datatypes.pyx --force
cython -a --cplus common/encoding.pyx --force
cython -a --cplus common/print_helpers.pyx --force
cython -a --cplus transport/relay.pyx --force
cython -a --cplus transport/node.pyx --force
cython -a --cplus transport/dispatch.pyx --force

# general compile of project modules
python3.6 setup.py build_ext --inplace --force

