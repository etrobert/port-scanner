from port_scanner.port_scanner import main
import pytest
from unittest import mock
import sys


def assert_exit(args, code):
    __tracebackhide__ = True
    with mock.patch.object(sys, 'argv', args):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == code


def test():
    # TODO Specify sys.argv
    assert_exit(["port_scanner", "-h"], 0)
    assert_exit(["port_scanner"], 2)
