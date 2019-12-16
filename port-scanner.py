#!/usr/bin/python

import subprocess
import sys
import os


def new_filename(pattern):
    """Returns the first filename matching pattern for which a file does not exist
    :param pattern: a pattern of the form *%s*
    """
    i = 0
    while os.path.exists(pattern % i):
        i += 1
    return pattern % i


if __name__ == "__main__":
    tmp_filename = new_filename(".scan%s.xml")
    returncode = subprocess.call(
        ["nmap",
         "-v",
         "-sV",
         "-Taggressive",
         "--script=vulscan/vulscan.nse",
         "-oX", tmp_filename] + sys.argv[1:])
    # if nmap encountered an error, terminate
    if returncode:
        sys.exit()
    try:
        html_filename = new_filename("scan%s.html")
        subprocess.call(["xsltproc", tmp_filename, "-o", html_filename])
        print("Scan successfull. Results are in: " + html_filename)
    finally:
        os.remove(tmp_filename)
