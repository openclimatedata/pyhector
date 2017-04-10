# Releasing a `pyhector` version to PyPI

## Changelog

Make sure the [changelog](CHANGELOG.md) is updated with the latest note-worthy
changes.

## Tag a Release

`pyhector` uses a "v<major>.<minor>.<patch>" format, for example:

    git tag v1.0.0

## Testing on TestPyPI

Run

    make publish-on-testpypi

and then

    make test-testpypi-install

to publish and test `pyhector` on PyPI's testing instance.

Once done the releases can be removed from the testing instance on
https://testpypi.python.org/

## Publish on PyPI

Make sure the last commit in the repository is the tagged one.

Then, run

    make publish-on-pypi

and then

    make test-pypi-install

to publish and test `pyhector` on PyPI.

## Alternative Manual steps

### Registering on PyPI

Assuming a `.pypirc` is set with "pypi".

    [pypi]
    repository=https://pypi.python.org/pypi

The first time one needs to register on PyPI with

    python setup.py register -r pypi

### Release on PyPI

    python setup.py sdist upload -r pypi

### Testing

Check if `pyhector` can be installed from PyPI:

    pip install pyhector --upgrade

## Notebook

Make sure the Jupyter Notebook is up-to date with the latest version. The
notebook can be re-compiled at
<http://mybinder.org/status/openclimatedata/pyhector>.
