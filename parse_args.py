import argparse
import ipaddress
import re

hostname_label_regex = r"(?!-)[a-zA-Z\d-]{1,63}(?<!-)"
hostname_regex = r"(?=^.{1,253}\.?$)(" + hostname_label_regex + r"\.)*" + \
    r"(" + hostname_label_regex + r"\.?)"
ipv4_regex = r"(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
# Source: https://stackoverflow.com/questions/53497/regular-expression-that-matches-valid-ipv6-addresses
ipv6_regex = r"([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])"
ip_regex = r"(" + ipv4_regex + r")|(" + ipv6_regex + r")"
cidr_regex = r"\/([0-9]|[1-2][0-9]|3[0-2])"
target_regex = r"((" + hostname_regex + r")|(" + ip_regex + r"))" + \
    r"(" + cidr_regex + r")?"


def is_valid_hostname(hostname):
    return re.compile(hostname_regex + r"$").match(hostname)


def is_valid_ip(ip):
    return re.compile(ip_regex + r"$").match(ip)


def is_valid_target(target):
    return re.compile(target_regex + r"$").match(target)


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
