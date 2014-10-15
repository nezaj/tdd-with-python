#!/usr/bin/env python

from setuptools import setup, find_packages

dependencies = [
    # packages for which we want latest stable version
    "pep8>=1.5.6",
    "pylint>=1.2.1",
    "selenium>=2.43.0",
    # Additional packages
    "Django==1.7"
]

setup(
    name="superlists",
    version="1.0",
    url="https://github.com/nezaj/tdd-with-python/tree/master/superlists",
    packages=find_packages(),
    install_requires=dependencies,
    use_2to3=True
)
