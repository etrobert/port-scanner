from toolbox import assert_exit
from netns_sandbox import NetNSSandbox

from bs4 import BeautifulSoup

try:
    import http.server as BaseHTTPServer
except:
    import BaseHTTPServer
import threading

try:
    import html  # Python3
except ImportError:
    import HTMLParser  # Python2


def assert_open_count(filename, count):
    soup = BeautifulSoup(open(filename), features="html.parser")
    assert len(soup.find_all(class_="open")) == count


def test_netns():
    test_filename = "test.html"

    with NetNSSandbox():
        assert_exit(["port_scanner", "localhost", "-o", test_filename], 0)
        assert_open_count(test_filename, 0)

        webserver = BaseHTTPServer.HTTPServer(
            ('', 8000), BaseHTTPServer.BaseHTTPRequestHandler)
        threading.Thread(target=webserver.serve_forever).start()
        assert_exit(["port_scanner", "localhost", "-o", test_filename], 0)
        webserver.shutdown()
        assert_open_count(test_filename, 1)
