from __future__ import print_function
import subprocess
import sys
import os
import distutils.spawn
from .parse_args import parse_args


def test_requirements():
    required_programs = ["nmap", "xsltproc"]
    missing_programs = [
        name for name in required_programs if not distutils.spawn.find_executable(name)]
    if missing_programs:
        print("Error: the following executable dependencies are missing:",
              " ".join(missing_programs), file=sys.stderr)
        exit(2)


def main():
    test_requirements()
    arguments = parse_args()
    tmp_filename = "." + arguments.outfile + ".xml"
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
        subprocess.call(["xsltproc", tmp_filename, "-o", arguments.outfile])
        print("Scan successfull. Results are in: " + arguments.outfile)
    finally:
        os.remove(tmp_filename)
