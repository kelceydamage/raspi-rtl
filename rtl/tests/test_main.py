"""Test case for main.py"""
import argparse
import subprocess
import time
import os
from unittest import mock
import pytest
from rtl.main import main
from rtl.main import launch
from rtl.main import embedded_parser
from rtl.main import service_wrapper


MOCK_PIDFILES = [
    'master',
    'RELAY',
    'TASK',
    'TASK',
    'TASK'
]


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(meta=False, no_server=True)
)
def test_main(mock_args):
    """Test main.py"""
    result = main(mock_args.return_value)
    assert result


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(meta=True, no_server=False)
)
def test_print_meta(mock_args):
    """Test main.py"""
    with pytest.raises(SystemExit):
        assert main(mock_args.return_value)


def test_print_meta_alt():
    """Test main.py"""
    call = subprocess.call('rtl/main.py -m', shell=True)
    assert call == 1


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(meta=False, no_server=False)
)
def test_embedded_parser(mock_args):
    """Test main.py"""
    namespace = embedded_parser()
    assert namespace == mock_args.return_value


def test_service_wrapper():
    """Test main.py"""
    with pytest.raises(Exception):
        assert service_wrapper('bob')


def test_launch_error():
    """Test main.py"""
    with pytest.raises(Exception):
        assert launch('TaskNode', 0)


def test_pidfile_creation():
    """Ensure pidfiles get created"""
    time.sleep(0.5)
    pidfiles = os.listdir(os.path.expanduser('~/var/run'))
    test = [x.split('-')[0] for x in pidfiles]
    assert test == MOCK_PIDFILES


@pytest.yield_fixture
def delete_pid_files():
    """Delete pid files"""
    time.sleep(1)
    yield subprocess.check_call(['rm -rf ~/var/run/*'], shell=True)


def test_cleanup(delete_pid_files):
    """Clean up processes files created by tests"""
    assert delete_pid_files == 0
