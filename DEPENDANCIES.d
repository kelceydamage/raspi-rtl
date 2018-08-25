# Ubuntu 16.04, L4T, Tegra TX2

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
pip install ujson
pip install pyzmq
pip install lmdb
```

# Centos7.4+

### Development Environment & Core
```
sudo yum install python36u-pip python36u-devel python36u-setuptools
sudo yum install zeromq-devel-4.1.4-5.el7.x86_64 zeromq-4.1.4-5.el7.x86_64
```

### Virtual Environment
```bash
pip3.6 install virtualenv
virtualenv -p $(which python3.6) ~/python36
source ~/python36/bin/activate
```

### Required (within virtual env)
```
pip install ujson
pip install pyzmq
pip install lmdb
```
