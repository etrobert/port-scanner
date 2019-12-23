import subprocess
import sys
import os
from distutils.spawn import find_executable
from .parse_args import parse_args


def new_filename(pattern):
    """Returns the first filename matching pattern for which a file does not exist
    :param pattern: a pattern of the form *%s*
    """
    i = 0
    while os.path.exists(pattern % i):
        i += 1
    return pattern % i


def test_requirements():
    required_programs = ["nmap", "xsltproc"]
    missing_programs = [
        name for name in required_programs if not find_executable(name)]
    if missing_programs:
        print("Error: the following executable dependencies are missing:",
              " ".join(missing_programs), file=sys.stderr)
        exit(2)


def main():
    test_requirements()
    arguments = parse_args()
    tmp_filename = new_filename(".scan%s.xml")
    returncode = subprocess.call(
        ["nmap",
         "-v",
         "-sV",
         "-Taggressive",
         "--script=vulscan/vulscan.nse",
         "-oX", tmp_filename] + arguments.target)
    # if nmap encountered an error, terminate
    if returncode:
        sys.exit(returncode)
    try:
        html_filename = new_filename("scan%s.html")
        subprocess.call(["xsltproc", tmp_filename, "-o", html_filename])
        print("Scan successfull. Results are in: " + html_filename)
    finally:
        os.remove(tmp_filename)
