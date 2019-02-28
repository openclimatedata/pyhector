.. include:: ../README.rst
    :start-after: sec-begin-development
    :end-before: sec-end-development

Updating the Hector model version used
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **Hector** model source code is included in the **pyhector**
repository as a submodule. To update its version do the following:

1. If you didn't clone **pyhector** recursively:

    .. code:: bash

        git submodule update --init

2. Go into the ``hector`` folder and checkout the version to be used
   (replace ``VERSIONTAG`` according to the corresponding version
   tag):

    .. code:: bash

        cd hector
        git checkout VERSIONTAG

3. Commit the updated submodule to **pyhector**:

    .. code:: bash

        cd ..
        git add hector
        git commit -m

4. Please do not forget to run the tests with the new version.


.. include:: ../CONTRIBUTING.rst
