# Inspired by the python-netns documentation
# https://github.com/larsks/python-netns

import netns
import subprocess


def run_steps(steps, ignore_errors=False):
    """Runs the system commands specified in steps.

    If ignore_errors is set to True, continues upon failed commands,
    else throws subprocess.CalledProcessError.
    """

    for step in steps:
        try:
            print('+ {}'.format(step))
            subprocess.check_call(step, shell=True)
        except subprocess.CalledProcessError:
            if ignore_errors:
                pass
            else:
                raise


class NetNSSandbox():
    """Network Sandbox Context Manager using Linux Network Namespaces.

    Requires root access. Requires to be ran on a Linux distribution.
    Requires for the name "sandbox" not to be taken
    by an already existing Linux Network Namespace.
    """

    def __init__(self):
        run_steps([
            # create a network namespace named "sandbox"
            'ip netns add sandbox',
            # make the loopback interface UP
            'ip netns exec sandbox ip link set dev lo up',
        ])
        self.ns = netns.NetNS(nsname="sandbox")

    def __enter__(self):
        self.ns.__enter__()

    def __exit__(self, type, value, traceback):
        self.ns.__exit__()
        run_steps(["ip netns del sandbox"], ignore_errors=True)
