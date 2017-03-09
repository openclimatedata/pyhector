.. pyhector documentation master file, created by
   sphinx-quickstart on Thu Mar  9 15:08:38 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyhector
========

.. image:: https://img.shields.io/travis/openclimatedata/pyhector.svg
    :target: https://travis-ci.org/openclimatedata/pyhector

.. image:: https://img.shields.io/pypi/pyversions/pyhector.svg
    :target: https://pypi.python.org/pypi/pyhector

.. image:: https://img.shields.io/pypi/v/pyhector.svg
    :target: https://pypi.python.org/pypi/pyhector

.. image:: https://img.shields.io/badge/launch-binder-e66581.svg
    :target: http://mybinder.org/repo/openclimatedata/pyhector


**pyhector** is a Python interface for the simple global climate
carbon-cycle model `Hector <https://github.com/JGCRI/hector>`_.

**pyhector** makes the simple climate model Hector easily installable and usable
from Python and can for example be used in the analysis of mitigation scenarios,
in integrated assessment models, complex climate model emulation, and
uncertainty analyses.

`Hector <https://github.com/JGCRI/hector>`_ is written in C++ and developed at the
`Pacific Northwest National Laboratory <https://www.pnl.gov/>`_.

The model description is published in

  Hartin, C. A., Patel, P., Schwarber, A., Link, R. P., and Bond-Lamberty, B. P.: A simple object-oriented and open-source model for scientific and policy analyses of the global climate system – Hector v1.0, Geosci. Model Dev., 8, 939-955, `https://doi.org/10.5194/gmd-8-939-2015 <https://dx.doi.org/10.5194/gmd-8-939-2015>`_, 2015.

See the Hector `repository <https://github.com/JGCRI/hector>`_ and
`wiki <https://github.com/JGCRI/hector/wiki>`_ for further information.

The Python interface **pyhector** is developed by `Sven Willner <http://www.pik-potsdam.de/~willner/>`_
and `Robert Gieseke <https://www.pik-potsdam.de/members/gieseke>`_ at the
`Potsdam Institute for Climate Impact Research <https://www.pik-potsdam.de/>`_.

It is currently based on a
`slightly modified Hector version <https://github.com/swillner/hector/>`_ and
a `generic wrapper <https://github.com/swillner/hector-wrapper/>`_ for Hector's API.
See the included git submodules for the specific commits that are being used.

Basic example
-------------

::

    import pyhector

    output = pyhector.run(pyhector.rcp26)

Advanced example
----------------

::

    import pyhector
    from pyhector import rcp26, rcp45, rcp60, rcp85

    import matplotlib.pyplot as plt

    for rcp in [rcp26, rcp45, rcp60, rcp85]:
        output = pyhector.run(rcp, {"core": {"endDate": 2100}})
        temp = output["temperature.Tgav"]
        # Adjust to 1850 - 1900 reference period
        temp = temp.loc[1850:] - temp.loc[1850:1900].mean()
        temp.plot(label=rcp.name.split("_")[0])
    plt.title("Global mean temperature")
    plt.ylabel("°C over pre-industrial (1850-1900 mean)")
    plt.legend(loc="best")


.. image:: example-plot.png

API docs
--------

.. toctree::
   :maxdepth: 2

   pyhector
