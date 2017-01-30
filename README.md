# pyhector

[![Build Status](https://img.shields.io/travis/swillner/pyhector.svg)](https://travis-ci.org/swillner/pyhector)

## Development

For local development you can clone the repository, update the dependencies
and install in a Virtualenv with pip.

```bash
git clone https://github.com/swillner/pyhector.git
cd pyhector
git submodule update --init --recursive
python3 -v venv venv
./venv/bin/pip install --editable .
```

After updating the repository with `git pull` you need to also update the
submodule with the command above.

Tests can be run locally with

```bash
./venv/bin/pytest tests
```
