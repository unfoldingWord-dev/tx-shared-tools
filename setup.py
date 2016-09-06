from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), "r") as f:
    long_description = f.read()

setup(
    name="tx-shared-tools",
    version="1.0.0",
    description="A python library for shared tools",
    long_description=long_description,
    url="https://github.com/unfoldingWord-dev/tx-shared-tools",
    author="unfoldingWord",
    author_email="richard_mahn@wycliffeassociates.org"
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords=["unfoldingword", "tx", "toops"],
    packages=find_packages(),
    install_requires=["future", "requests"],
    test_suite="tests"
)
