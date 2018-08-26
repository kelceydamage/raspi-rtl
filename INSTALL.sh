#! /bin/bash
# Ghetto install script! Yes this sucks, yes this is an afterthought.

if [ -f /etc/os-release ] 
then
    . /etc/os-release
else
    echo "ERROR: I need the file /etc/os-release to determine what my distribution is..."
    exit
fi
echo -e "Found: $ID\nInstalling\n"
if [ $ID == ubuntu ] 
then
    sudo apt-get install perl wheel build-essential libzmq3-dev
    sudo apt-get install python3-setuptools python3-dev python3-pip 

    pip3 install virtualenv
    virtualenv -p $(which python3) ~/python3
    source ~/python3/bin/activate
else
    sudo yum install python36u-pip python36u-devel python36u-setuptools
    sudo yum install zeromq-devel-4.1.4-5.el7.x86_64 zeromq-4.1.4-5.el7.x86_64

    pip3.6 install virtualenv
    virtualenv -p $(which python3) ~/python36
    source ~/python36/bin/activate
fi

pip install ujson
pip install pyzmq
pip install lmdb
