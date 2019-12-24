from port_scanner.port_scanner import main
import pytest
import sys
import distutils.spawn

try:
    from unittest import mock
except ImportError:
    import mock


def run_with_args(args):
    __tracebackhide__ = True
    with mock.patch.object(sys, 'argv', args):
        main()


def assert_exit(args, code):
    __tracebackhide__ = True
    try:
        run_with_args(args)
        assert code == 0
    except SystemExit as se:
        assert se.code == code


def test_return_codes():
    assert_exit(["port_scanner", "-h"], 0)
    assert_exit(["port_scanner", "--help"], 0)
    assert_exit(["port_scanner", "-h", "hostname"], 0)
    assert_exit(["port_scanner", "-f", "emptyfile"], 0)
    assert_exit(["port_scanner", "-f", "missingfile"], 2)
    assert_exit(["port_scanner", "--this-is-fake"], 2)
    assert_exit(["port_scanner", "-b"], 2)
    assert_exit(["port_scanner", "-hb"], 2)
    assert_exit(["port_scanner"], 2)
    assert_exit(["port_scanner", "host.not.found"], 0)


def test_dependancy():
    assert_exit(["port_scanner", "host.not.found"], 0)
    original_find_executable = distutils.spawn.find_executable
    with mock.patch.object(
            distutils.spawn, 'find_executable',
            lambda name: None if name == "nmap" else original_find_executable(name)):
        assert_exit(["port_scanner", "host.not.found"], 2)
