Changelog
---------

2.4.0.0
~~~~~~~
- update to Hector 2.4.0 (revamped multi-biome system)

2.3.1.0
~~~~~~~
- update to Hector 2.3.1

2.3.0.0
~~~~~~~

- fix ``__hector_version__`` field
- update to Hector 2.3.0 (https://github.com/JGCRI/hector/releases/tag/v2.3.0)

2.2.2.0
~~~~~~~

- update to Hector 2.2.2 (https://github.com/JGCRI/hector/releases/tag/v2.2.2)
- includes new output variables from Hector 2.2.1

2.2.0.1
~~~~~~~

- fix installation

2.2.0.0
~~~~~~~

- update to Hector 2.2.0 (https://github.com/JGCRI/hector/releases/tag/v2.2.0)
- add a new parameter "VOLCANIC_SCALE"

2.1.0.0
~~~~~~~

- switch to new versioning scheme:
  Hector version + ascending number denoting changes in Pyhector

2.1.0a
~~~~~~

- update to Hector 2.1.0 (https://github.com/JGCRI/hector/releases/tag/v2.1.0)
- switch to new versioning scheme:
  Hector version + ascending letters denoting changes in Pyhector

2.1.3
~~~~~

- C++ bindings are using `pybind11 <https://github.com/pybind/pybind11>`_ now
  (making the hector-wrapper obsolete)
- drop offical support for 2.7 and 3.4 (not tested anymore)
- new in Pyhector: ``shutdown``, ``run(until=None)``, ``__hector_version__``, ``clear_observables``, ``reset``

2.0.1
~~~~~

- updated to Hector 2.0.1 (license clarification)

2.0.0
~~~~~

- updated to Hector 2.0.0
- directly works with Hector, no fork needed anymore
- see the Hector changelog for details (https://github.com/JGCRI/hector/releases)

0.9.0
~~~~~

- include more forcings as output variables

0.8.1
~~~~~

-  updated underlying Hector version to include the fix for
   halo carbon double counting (https://github.com/JGCRI/hector/pull/201)

0.7.0
~~~~~

-  overhauled docs to include tables for configuration dicts
-  fixed start_date bug when not setting observables

0.6.0
~~~~~

-  explicitly state C++11 in ``setup.py``
-  enable spinup output to be readable

0.5.2
~~~~~

-  config dictionary can also take a Pandas series instead of list of
   tuples for time series
-  add function to export scenarios as CSV files (in Hector format)
-  add API docs using Sphinx and Readthedocs

0.4.0
~~~~~

-  return ``parameters`` only when requested in ``run`` function
-  allow different configuration objects to be used

0.3.0
~~~~~

-  default config object uses Python numbers or booleans instead of
   strings, units can be included as tuples like ``(35.0, 'pptv')`` and
   time series as lists of tuples like
   ``'N2ON_emissions': [(1765, 11), (2000, 8), (2300, 8)]``

0.2.4
~~~~~

-  first PyPI beta release
