Releasing a ``pyhector`` version to PyPI
========================================

Changelog
---------

Make sure the `changelog <CHANGELOG.rst>`__ is updated with the latest
note-worthy changes.

Tag a Release
-------------

``pyhector`` uses a “v...” format, for example:

::

   git tag v2.1.0.5

This is the 6th (starting from zero) version of Pyhector for version
2.1.0 of Hector. Both bug fixes or API changes (which should be rare)
are denoted by increasing the last digit.

Publishing on PyPI
------------------

Releases are automatically published on PyPI when a version tag is
pushed to GitHub.

Testing on TestPyPI
~~~~~~~~~~~~~~~~~~~

If necessary, the packaging process can be tested on PyPI’s testing
instance.

Run

::

   make publish-on-testpypi

and then

::

   make test-testpypi-install

to publish and test the ``pyhector`` installation process.

Once done the releases can be removed from the testing instance on
https://testpypi.python.org/

Notebook
--------

Make sure the Jupyter Notebook is up-to date with the latest version.
The notebook can be re-compiled at http://mybinder.org/.
