# pyhector

[![Build Status](https://img.shields.io/travis/swillner/pyhector.svg)](https://travis-ci.org/swillner/pyhector)

`pyhector` is a Python wrapper for the simple global climate carbon-cycle model
[Hector](https://github.com/JGCRI/hector).

## Development

For local development you can clone the repository, update the dependencies
and install in a Virtualenv with pip.

```bash
git clone https://github.com/swillner/pyhector.git --recursive
cd pyhector
python3 -m venv venv
./venv/bin/pip install --editable .
```

To update `pyhector` and all submodules you can run
```
git pull --recurse-submodules
```

Tests can be run locally with

```bash
./venv/bin/pytest tests
```
