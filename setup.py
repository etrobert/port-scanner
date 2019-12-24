from setuptools import setup, find_packages

setup(
    name="port_scanner",
    version="0.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'port_scanner = port_scanner.port_scanner:main'
        ]
    },
    install_requires=['py2-ipaddress;python_version<"3"']
)
