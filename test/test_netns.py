import netns
import subprocess

from toolbox import assert_exit

from bs4 import BeautifulSoup

try:
    import html  # Python3
except ImportError:
    import HTMLParser  # Python2


def run_steps(steps, ignore_errors=False):
    for step in steps:
        try:
            print('+ {}'.format(step))
            subprocess.check_call(step, shell=True)
        except subprocess.CalledProcessError:
            if ignore_errors:
                pass
            else:
                raise


def assert_open_count(filename, count):
    soup = BeautifulSoup(open(filename), features="html.parser")
    assert len(soup.find_all(class_="open")) == count


def test_netns():
    test_filename = "test.html"
    try:
        run_steps([
            # create a network namespace named "sandbox"
            'ip netns add sandbox',
            # make the loopback interface UP
            'ip netns exec sandbox ip link set dev lo up',
        ])
        with netns.NetNS(nsname="sandbox"):
            assert_exit(["port_scanner", "localhost", "-o", test_filename], 0)
            assert_open_count(test_filename, 0)
    finally:
        run_steps(["ip netns del sandbox"], ignore_errors=True)
