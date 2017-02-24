# Releasing a `pyhector` version to PyPI

## Changelog

Make sure the [changelog](CHANGELOG.md) is updated with the latest note-worthy
changes.

## Tag a Release

`pyhector` uses a "v<major>.<minor>.<patch>" format, for example:

    git tag v1.0.0

## Registering on PyPI

The first time one needs to register on PyPI with

    python setup.py register -r pypi


## Release on PyPI

    python setup.py sdist upload -r pypi
