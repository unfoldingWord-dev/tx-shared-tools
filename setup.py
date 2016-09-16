import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(f_name):
    return open(os.path.join(os.path.dirname(__file__), f_name)).read()


setup(
    name="tx-shared-tools",
    version="0.0.1",
    author="unfoldingWord",
    author_email="unfoldingword.org",
    description="A collection of useful scripts for tX",
    license="MIT",
    keywords="unfoldingWord python tools tx",
    url="https://github.org/unfoldingWord-dev/tx-shared-tools",
    packages=['general_tools', 'aws', 'client', 'converter', 'door43', 'manager'],
    long_description=read('README.rst'),
    classifiers=[],
    requires=['pygithub', ]
)
