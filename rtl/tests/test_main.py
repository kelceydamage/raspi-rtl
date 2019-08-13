#! /usr/bin/env python
# ------------------------------------------------------------------------ 79->
# Author: ${name=Kelcey Damage}
# Python: 3.5+
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Doc
# ------------------------------------------------------------------------ 79->
"""Pytest module for testing the rtl.main module."""


# Imports
# ------------------------------------------------------------------------ 79->
import argparse
import subprocess
import time
import os
from unittest import mock
import pytest
from rtl.main import Launcher
from rtl.main import StartError
from rtl.main import _service_wrapper


# Const
# ------------------------------------------------------------------------ 79->
MOCK_PIDFILES = [
    'master',
    'RELAY',
    'TASK',
    'TASK',
    'TASK'
]
META_PRINT = (
    '--------------------------------------------------------------------'
    '-----------\nREGISTERED-TASKS:\n------------------------------------'
    '-------------------------------------------\n \x1b[48;5;6m\x1b[38;5;'
    '0m__\x1b[m \x1b[38;5;14mnull\x1b[m\n--------------------------------'
    '-----------------------------------------------\n'
)


# Functions
# ------------------------------------------------------------------------ 79->
@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(meta=False, no_server=True)
)
def test_run(mock_args):
    """Test running the main function similar to calling python -m rtl.main -m.
    It should exit cleanly with SystemExit and no errors.

    Args:
        mock_args (Namespace): argparse namespace.
        mock_args.meta (bool): True to print metadata and exit, False to
            continue script.
        mock_args.no_server (bool): True to disable actual launching/keep-alive
            of rtl nodes, False to allow script to keep alive.

    """
    launcher = Launcher()
    launcher.args = mock_args.return_value
    with pytest.raises(SystemExit):
        assert launcher.run()


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(meta=True, no_server=False)
)
def test_print_meta_run(mock_args):
    """Test the print_meta function by ensuring it returns SystemExit.

    Args:
        mock_args (Namespace): argparse namespace.
        mock_args.meta (bool): True to print metadata and exit, False to
            continue script.
        mock_args.no_server (bool): True to disable actual launching/keep-alive
            of rtl nodes, False to allow script to keep alive.

    """
    launcher = Launcher()
    launcher.args = mock_args.return_value
    with pytest.raises(SystemExit):
        assert launcher.run()


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(meta=True, no_server=False)
)
def test_print_meta_print(mock_args, capsys):
    """Test the print_meta function by ensuring the output is as expected in the
    CI environment (null task only).

    Args:
        mock_args (Namespace): argparse namespace.
        mock_args.meta (bool): True to print metadata and exit, False to
            continue script.
        mock_args.no_server (bool): True to disable actual launching/keep-alive
            of rtl nodes, False to allow script to keep alive.

        capsys (object): system IO capture object for comparing the output of
            print functions.

    """
    launcher = Launcher()
    launcher.args = mock_args.return_value
    try:
        launcher.run()
    except SystemExit:
        pass
    finally:
        out, _ = capsys.readouterr()
        assert out.encode() == META_PRINT.encode()


def test_print_meta_alt():
    """Test the print_meta function by calling directly from the command
    line.

    """
    call = subprocess.call('rtl/main.py -m', shell=True)
    assert call == 1


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(meta=False, no_server=False)
)
def test_embedded_parser(mock_args):
    """Test embedded argparse parser by ensuring the generated values match the
    type and composition of the mock namespace.

    Args:
        mock_args (Namespace): argparse namespace.
        mock_args.meta (bool): True to print metadata and exit, False to
            continue script.
        mock_args.no_server (bool): True to disable actual launching/keep-alive
            of rtl nodes, False to allow script to keep alive.

    """
    launcher = Launcher()
    assert launcher.args == mock_args.return_value


def test_service_wrapper():
    """Test service wrapper (which calls SomeClass().run() inside a subprocess)
    by ensuring it properly fails if it were to receive a class name that isn't
    loaded into the module namespace.

    """
    with pytest.raises(StartError):
        assert _service_wrapper('bob')


def test_launch_error():
    """Test the launcher by passing it a count of 0 nodes to start."""
    launcher = Launcher()
    assert not launcher._launch('TaskNode', 0)


def test_start_node():
    """Test the start node private method."""
    launcher = Launcher()
    assert not launcher._start_node('TaskNode', 1)


def test_pidfile_creation():
    """Test that all nodes correctly create pidfiles when they are instantiated.

    """
    time.sleep(0.5)
    pidfiles = os.listdir(os.path.expanduser('~/var/run'))
    test = [x.split('-')[0] for x in pidfiles]
    assert test.sort() == MOCK_PIDFILES.sort()


@pytest.yield_fixture
def delete_pid_files():
    """Fixture to delete pidfiles after tests run.

    Note:
        Only use if there are no rtl subprocesses running.

    """
    time.sleep(1)
    yield subprocess.check_call(['rm -rf ~/var/run/*'], shell=True)


def test_cleanup(delete_pid_files):
    """Cleanup the test environment."""
    assert delete_pid_files == 0

# Main
# ------------------------------------------------------------------------ 79->
