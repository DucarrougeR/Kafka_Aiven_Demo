#!/usr/bin/env python
import sys
import setuptools

if sys.version_info < (3, 9):
    print('Please upgrade to Python 3.9 or higher to run this code.')
    sys.exit(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Romain-Aiven-Homework",
    version="0.0.1",
    author="Romain Ducarrouge",
    author_email="romain@aiven.com",
    description="Kafka topics to Aiven PostgrSQL data store.",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
