Changelog
---------

0.5.2
~~~~~~~~~~~~~~~~~~~

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
