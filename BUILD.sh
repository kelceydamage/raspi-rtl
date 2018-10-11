# setenv
source ~/python3/bin/activate

# If GIT_HOME is not set to the root location of your git folder globally, you can set here.
# GIT_HOME=~/git

# Project/repo folder within your git home dir.
PROJECT_DIR=rtl

# Pre compile function for writing clean cpp file.
function pre_compile() {
    cython -a --cplus $1 --force --include-dir $GIT_HOME/$PROJECT_DIR
}

PYX_FILES=(
    common/datatypes.pyx
    common/encoding.pyx
    common/print_helpers.pyx
    transport/relay.pyx
    transport/node.pyx
    transport/dispatch.pyx
    )

# precompile c++ modules
for i in ${PYX_FILES[@]}; do
    echo -e "Pre-compiling: $i"
    pre_compile $i
done

# general compile of project modules
echo -e "Starting full compile"
python setup.py build_ext --inplace --force
