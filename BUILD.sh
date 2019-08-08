ROOT=rtl/

# setenv
#source ~/python3/bin/activate

# If GIT_HOME is not set to the root location of your git folder globally, you can set here.
# GIT_HOME=~/git
GIT_HOME=/git/projects/personal

# Project/repo folder within your git home dir.
PROJECT_DIR=rtl/

# Pre compile function for writing clean cpp file.
function pre_compile() {
    cython -a --cplus $1 --force --include-dir $GIT_HOME/$PROJECT_DIR
}

PYX_FILES=(
    "${PROJECT_DIR}common/datatypes.pyx"
    "${PROJECT_DIR}common/encoding.pyx"
    "${PROJECT_DIR}common/print_helpers.pyx"
    "${PROJECT_DIR}common/normalization.pyx"
    "${PROJECT_DIR}common/regression.pyx"
    "${PROJECT_DIR}common/transform.pyx"
    "${PROJECT_DIR}common/task.pyx"
    "${PROJECT_DIR}transport/relay.pyx"
    "${PROJECT_DIR}transport/node.pyx"
    "${PROJECT_DIR}transport/dispatch.pyx"
    "${PROJECT_DIR}tasks/open_array.pyx"
    "${PROJECT_DIR}tasks/normalize.pyx"
    )

# precompile c++ modules
for i in ${PYX_FILES[@]}; do
    echo -e "Pre-compiling: $i"
    pre_compile $i
done

# general compile of project modules
echo -e "Starting full compile"
python setup.py build_ext --inplace --force
