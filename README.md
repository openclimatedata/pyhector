# pyhector

[![Build Status](https://img.shields.io/travis/swillner/pyhector.svg)](https://travis-ci.org/swillner/pyhector)

`pyhector` is a Python wrapper for the simple global climate
carbon-cycle model [Hector](https://github.com/JGCRI/hector).


## Prerequisites

[Hector](https://github.com/JGCRI/hector)
requires [Boost](http://www.boost.org/), so to install and use
`pyhector` you need to have the filesystem and system modules
of *Boost version 1.5+* installed.

E.g., on Ubuntu/Debian these can be installed by invoking
```bash
sudo apt-get install libboost-filesystem-dev libboost-system-dev
```


## Development

For local development you can clone the repository, update the
dependencies and install in a Virtualenv with pip.

```bash
git clone https://github.com/swillner/pyhector.git --recursive
cd pyhector
python -m venv venv
./venv/bin/pip install --editable .
```

To update `pyhector` and all submodules you can run
```bash
git pull --recurse-submodules
```

Tests can be run locally with

```bash
python setup.py test
```
