#!/usr/bin/env python
import olpy

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    return open(filename).read()

setup(
    name="olpy",
    version=olpy.__version__,
    description="Python client for the Online Labs API",
    long_description=read("README.rst"),
    author="adebarbara",
    author_email="adebarbara@gmail.com",
    maintainer="Andres de Barbara",
    maintainer_email="adebarbara@gmail.com",
    url="https://github.com/adebarbara/olpy",
    download_url="https://github.com/adebarbara/olpy/archive/master.zip",
    classifiers=("Development Status :: 2 - Alpha",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2.6",
                 "Programming Language :: Python :: 2.7"),
    license=read("LICENSE"),
    packages=['olpy'],
    install_requires=["requests >= 1.0.4"],
)
