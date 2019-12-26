import netns
import subprocess

from toolbox import run_with_args

from bs4 import BeautifulSoup

try:
    import html  # Python3
except ImportError:
    import HTMLParser  # Python2


def run_steps(steps, ignore_errors=False):
    __tracebackhide__ = True
    for step in steps:
        try:
            print('+ {}'.format(step))
            subprocess.check_call(step, shell=True)
        except subprocess.CalledProcessError:
            if ignore_errors:
                pass
            else:
                raise


def run_with_netns(setup, teardown, args):
    __tracebackhide__ = True
    try:
        run_steps(setup)

        with netns.NetNS(nsname="sandbox"):
            run_with_args(args)
    finally:
        run_steps(teardown, ignore_errors=True)


def assert_open_count(filename, count):
    __tracebackhide__ = True
    soup = BeautifulSoup(open(filename), features="html.parser")
    assert len(soup.find_all(class_="open")) == count


def test_netns():
    test_filename = "test.html"
    run_with_netns(
        setup=[
            # create a network namespace named "sandbox"
            'ip netns add sandbox',
            # make the loopback interface UP
            'ip netns exec sandbox ip link set dev lo up',
        ],
        teardown=['ip netns del sandbox'],
        args=["port_scanner", "localhost", "-o", test_filename])
    assert_open_count(test_filename, 0)
