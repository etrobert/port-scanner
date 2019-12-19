from parse_args import is_valid_hostname, is_valid_ip, is_valid_target


def test_is_valid_hostname_label_length():
    label_63 = "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"
    assert is_valid_hostname(label_63)
    assert not is_valid_hostname(label_63 + "u")
    assert not is_valid_hostname("")


def test_is_valid_hostname_length():
    label_49_dot = "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu."
    host_253 = label_49_dot + label_49_dot + \
        label_49_dot + label_49_dot + label_49_dot + "uuu"
    assert is_valid_hostname(host_253)
    assert is_valid_hostname(host_253 + ".")
    assert not is_valid_hostname(host_253 + "u")


def test_is_valid_hostname_dash():
    assert is_valid_hostname("a-b")
    assert is_valid_hostname("a---------b")
    assert not is_valid_hostname("-")
    assert not is_valid_hostname("----")
    assert not is_valid_hostname("-b")
    assert not is_valid_hostname("b-")


def test_is_valid_hostname_dot():
    assert is_valid_hostname("a.b.c.d.e.f.g.h.i.j.k.l.m.n")
    assert is_valid_hostname("a.")
    assert not is_valid_hostname(".a")
    assert not is_valid_hostname("a..")
    assert not is_valid_hostname(".")
    assert not is_valid_hostname("a..b")


def test_is_valid_hostname():
    assert is_valid_hostname("localhost")
    assert is_valid_hostname("LOCALHOST")
    assert is_valid_hostname("a")
    assert is_valid_hostname("google.com")
    assert is_valid_hostname("www.google.com")
    assert not is_valid_hostname("http://www.google.com")


def test_is_valid_ip():
    assert is_valid_ip("0.0.0.0")
    assert is_valid_ip("127.0.0.1")
    assert is_valid_ip("192.168.0.1")
    assert is_valid_ip("255.255.255.255")
    assert not is_valid_ip("")
    assert not is_valid_ip("hello")
    assert not is_valid_ip("www.google.com")
    assert not is_valid_ip("256.0.0.0")
    assert not is_valid_ip("999.999.999.999")
    assert not is_valid_ip("256")
    assert not is_valid_ip("0.0.0")
    assert not is_valid_ip("0.0.0.")
    assert not is_valid_ip("0.0.0.0.")
    assert not is_valid_ip("0.0.0.0.0")


def test_is_valid_target():
    assert is_valid_target("www.google.com")
    assert not is_valid_target("http://www.google.com")
    assert not is_valid_target("Id love myself some turkey")
    assert is_valid_target("0.0.0.0")
    assert is_valid_target("localhost")
    assert is_valid_target("0.0.0.0/0")
    assert is_valid_target("0.0.0.0/8")
    assert is_valid_target("0.0.0.0/16")
    assert is_valid_target("0.0.0.0/32")
    assert not is_valid_target("0.0.0.0/33")
    assert not is_valid_target("0.0.0.0/0/0")
    assert is_valid_target("localhost/15")
    assert not is_valid_target("localhost/99")
