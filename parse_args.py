import argparse
import ipaddress
import re

hostname_regex = r"^(?=^.{1,253}\.?$)((?!-)[a-zA-Z\d-]{1,63}(?<!-)\.)*((?!-)[a-zA-Z\d-]{1,63}(?<!-)\.?)$"


def is_valid_hostname(hostname):
    return re.compile(hostname_regex).match(hostname)


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    return True


def is_valid_target(target):
    split = target.split('/')
    if len(split) > 2 or len(split) < 1:
        return False
    if not is_valid_hostname(split[0]) and not is_valid_ip(split[0]):
        return False
    if len(split) == 2:
        try:
            cidr = int(split[1])
            if cidr < 0 or cidr > 32:
                return False
        except ValueError:
            return False
    return True


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
