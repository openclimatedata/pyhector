# pyhector

[![Build Status](https://img.shields.io/travis/swillner/pyhector.svg)](https://travis-ci.org/swillner/pyhector)
[![PyPI](https://img.shields.io/pypi/pyversions/pyhector.svg)](https://pypi.python.org/pypi/pyhector)
[![PyPI](https://img.shields.io/pypi/v/pyhector.svg)](https://pypi.python.org/pypi/pyhector)
[![Launch Binder](https://img.shields.io/badge/launch-binder-e66581.svg)](http://mybinder.org/repo/swillner/pyhector)

**pyhector** is a Python wrapper for the simple global climate
carbon-cycle model [Hector](https://github.com/JGCRI/hector).


## Install

### Prerequisites

[Hector](https://github.com/JGCRI/hector)
requires [Boost](http://www.boost.org/), so to install and use
**pyhector** you need to have the filesystem and system modules
of *Boost* version 1.52 or later installed (see also the
[Hector build instructions](https://github.com/JGCRI/hector/wiki/BuildHector)).

E.g., on Ubuntu/Debian these can be installed by invoking
```bash
sudo apt-get install libboost-filesystem-dev libboost-system-dev
```

### Install using pip

You can simply install **pyhector** from [PyPI](https://pypi.python.org/pypi/pyhector) by invoking
```bash
pip install pyhector
```


## Changelog

### Unreleased

- default config object uses Python numbers where possible instead
  of strings

### 0.2.4

- first PyPI beta release


## Development

For local development you can clone the repository, update the
dependencies and install in a virtual environment with `pip`.

```bash
git clone https://github.com/swillner/pyhector.git --recursive
cd pyhector
python3 -m venv venv
./venv/bin/pip install --editable .
```

To update **pyhector** and all submodules you can run
```bash
git pull --recurse-submodules
```

Tests can be run locally with

```
python setup.py test
```
