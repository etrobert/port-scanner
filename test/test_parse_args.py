from parse_args import is_valid_hostname

def test_is_valid_hostname_label_length():
  label_63 = "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"
  assert is_valid_hostname(label_63)
  assert not is_valid_hostname(label_63 + "u")
  assert not is_valid_hostname("")

def test_is_valid_hostname_length():
  label_49_dot = "uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu."
  host_253 = label_49_dot + label_49_dot + label_49_dot + label_49_dot + label_49_dot + "uuu"
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
  assert is_valid_hostname("a")
  assert is_valid_hostname("google.com")
  assert is_valid_hostname("www.google.com")
  assert not is_valid_hostname("http://www.google.com")
