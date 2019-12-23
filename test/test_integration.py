from port_scanner.port_scanner import main
import pytest
from unittest import mock
import sys


def assert_exit(args, code):
    __tracebackhide__ = True
    with mock.patch.object(sys, 'argv', args):
        try:
            main()
            assert code == 0
        except SystemExit as se:
            assert se.code == code


def test():
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
