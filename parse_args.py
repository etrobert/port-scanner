import argparse
import ipaddress
import re


def is_valid_hostname(hostname):
    # Updated from: https://stackoverflow.com/questions/2532053/validate-a-hostname-string#2532344
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    if len(hostname) > 253:
        return False
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def is_valid_interface(target):
    try:
        ipaddress.ip_interface(target)
    except ValueError:
        return False
    return True


def is_valid_target(target):
    # A valid IP address and a valid IP network are a valid IP interface
    # So the test for those is implicit
    return is_valid_hostname(target) or is_valid_interface(target)


def parse_target(target):
    if not is_valid_target(target):
        raise argparse.ArgumentTypeError(target + " is not a valid target")
    return target


def parse_targets_file(filename):
    try:
        file = open(filename, "r")
        # List comprehension is used to remove trailing newline
        lines = [target[:-1] for target in file.readlines()]
        for l in lines:
            if not is_valid_target(l):
                raise argparse.ArgumentTypeError(l + " is not a valid target")
        return lines
    except OSError as error:
        raise argparse.ArgumentTypeError(error.strerror)


def parse_args():
    parser = argparse.ArgumentParser()
    target_group = parser.add_argument_group(
        'target specification',
        'A target can be a hostname, IP address, network or interface'
    ).add_mutually_exclusive_group(required=True)
    target_group.add_argument("-f", "--file", type=parse_targets_file,
                              help="file containing newline separated targets")
    target_group.add_argument("target", default=[], type=parse_target,
                              nargs="*", help="target")
    args = parser.parse_args()
    if args.file is not None:
        args.target = args.file
        del args.file
    return args

