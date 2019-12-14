import subprocess
import sys
import os

def new_filename(pattern):
    i = 0
    while os.path.exists(pattern % i):
        i += 1
    return pattern % i

if __name__ == "__main__":
    tmp_filename = new_filename(".scan%s.xml")
    html_filename = new_filename("scan%s.html")
    returncode = subprocess.call(["nmap", "-v", "-sV", "-oX", tmp_filename] + sys.argv[1:])
    if returncode:
        sys.exit()
    subprocess.call(["xsltproc", tmp_filename, "-o", html_filename])
    os.remove(tmp_filename)

