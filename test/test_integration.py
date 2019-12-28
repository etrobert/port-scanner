from port_scanner.port_scanner import main
import pytest
import sys
import distutils.spawn
try:
    from unittest import mock
except ImportError:
    import mock

from toolbox import assert_exit

import subprocess
import netns

from bs4 import BeautifulSoup

try:
    import http.server as BaseHTTPServer  # Python3
except:
    import BaseHTTPServer  # Python2
import threading

try:
    import html  # Python3
except ImportError:
    import HTMLParser  # Python2

import os


def run_steps(steps, ignore_errors=False):
    """Runs the system commands specified in steps.

    If ignore_errors is set to True, continues upon failed commands,
    else throws subprocess.CalledProcessError.
    """

    for step in steps:
        try:
            print('+ {}'.format(step))
            subprocess.check_call(step, shell=True)
        except subprocess.CalledProcessError:
            if ignore_errors:
                pass
            else:
                raise


@pytest.fixture(scope="module")
def sandbox_netns():
    """Network Sandbox Fixture using Linux Network Namespaces.

    Requires root access. Requires to be ran on a Linux distribution.
    Requires for the name "sandbox" not to be taken
    by an already existing Linux Network Namespace.
    """
    run_steps([
        # create a network namespace named "sandbox"
        'ip netns add sandbox',
        # make the loopback interface UP
        'ip netns exec sandbox ip link set dev lo up',
    ])
    yield
    run_steps(["ip netns del sandbox"], ignore_errors=True)


@pytest.fixture
def empty_file():
    """File Fixture used to test program options.

    Requires the ability to create a file in the current folder.
    Requires a file named "emptyfile" not to be
    already present in the current folder.
    """
    if os.path.isfile("emptyfile"):
        raise Exception("emptyfile already exists")
    open("emptyfile", 'w').close()
    yield
    os.remove("emptyfile")


def test_options(empty_file):
    assert_exit(["port_scanner", "-h"], 0)
    assert_exit(["port_scanner", "--help"], 0)
    assert_exit(["port_scanner", "-h", "hostname"], 0)
    assert_exit(["port_scanner", "-f", "emptyfile"], 0)
    assert_exit(["port_scanner", "-f", "missingfile"], 2)
    assert_exit(["port_scanner", "--this-is-fake"], 2)
    assert_exit(["port_scanner", "-b"], 2)
    assert_exit(["port_scanner", "-hb"], 2)
    assert_exit(["port_scanner"], 2)


def test_dependancy(sandbox_netns):
    with netns.NetNS(nsname="sandbox"):
        assert_exit(["port_scanner", "host.not.found"], 0)
        original_find_executable = distutils.spawn.find_executable
        with mock.patch.object(
                distutils.spawn, 'find_executable',
                lambda name: None if name == "nmap" else original_find_executable(name)):
            assert_exit(["port_scanner", "host.not.found"], 2)


def assert_open_count(filename, count):
    soup = BeautifulSoup(open(filename), features="html.parser")
    assert len(soup.find_all(class_="open")) == count


@pytest.fixture
def http_server(sandbox_netns):
    with netns.NetNS(nsname="sandbox"):
        webserver = BaseHTTPServer.HTTPServer(
            ('', 8000), BaseHTTPServer.BaseHTTPRequestHandler)
        threading.Thread(target=webserver.serve_forever).start()
        yield
        webserver.shutdown()


def test_html(sandbox_netns):
    test_filename = "test.html"
    with netns.NetNS(nsname="sandbox"):
        assert_exit(["port_scanner", "localhost", "-o", test_filename], 0)
        assert_open_count(test_filename, 0)


def test_html_http_server(sandbox_netns, http_server):
    test_filename = "test.html"
    with netns.NetNS(nsname="sandbox"):
        assert_exit(["port_scanner", "localhost", "-o", test_filename], 0)
        assert_open_count(test_filename, 1)
