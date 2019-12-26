import sys

try:
    from unittest import mock
except ImportError:
    import mock

from port_scanner.port_scanner import main


def run_with_args(args):
    with mock.patch.object(sys, 'argv', args):
        main()


def assert_exit(args, code):
    try:
        run_with_args(args)
        assert code == 0
    except SystemExit as se:
        assert se.code == code
