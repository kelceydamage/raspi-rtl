[home](https://github.com/kelceydamage/rtl/blob/master/README.md)
# Ubuntu 16.04, L4T, Tegra TX2, AGX Xavier

### Development Environment
```bash
sudo apt-get install perl wheel build-essential libzmq3-dev
sudo apt-get install python3-setuptools python3-dev python3-pip
```

### Virtual Environment
```bash
pip3 install virtualenv
virtualenv -p $(which python3) ~/python3
source ~/python3/bin/activate
```

### Required (within virtual env)
```
pip3 install pyzmq pytest-cov python-coveralls codecov coverage lmdb cbor
pip3 install ujson numpy cython bokeh sklearn zmq sphinx
```

### Optional (for CUDA)
```
pip3 install fastrlock cupy
```

# Centos7.4+

### Development Environment & Core
```
sudo yum install centos-release-scl rh-python36
sudo yum install zeromq-devel zeromq
```

### Virtual Environment
```bash
pip3 install virtualenv
virtualenv -p $(which python3.6) ~/python3
source ~/python3/bin/activate
```

### Required (within virtual env)
```
pip3 install pyzmq pytest-cov python-coveralls codecov coverage lmdb cbor 
pip3 install ujson numpy cython bokeh sklearn zmq sphinx
```

### Optional (for CUDA)
```
pip3 install fastrlock cupy
```
