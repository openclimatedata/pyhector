.. automodule:: pyhector
    :members:
    :undoc-members:
    :show-inheritance:


pyhector.constants
------------------

Dictionaries ``components`` and ``variables`` used for mapping categories
internally. Auto-generated from Hector headers.


pyhector.default_config
-----------------------

A dictionary with Hector's default configuration parameters.
See also `the original config file on GitHub <https://github.com/openclimatedata/pyhector/blob/master/pyhector/rcp_default.ini>`_.
In **pyhector** this INI-file is represented as a dictionary.


pyhector.emissions
------------------

A dictionary with mapping from Hector components to emissions used in
the respective component.

.. include:: static/emissions_mapping.inc


pyhector.output
---------------

A dictionary with Hector's available output variables::

    output = {
        'C2F6_halocarbon.hc_concentration': {
            'component': 'C2F6_halocarbon',
            'description': 'C2F6 concentration',
            'unit': 'pptv',
            'variable': 'hc_concentration'
        },
        [...]

.. include:: static/output_variables.inc


pyhector.units
--------------

A dictionary with emissions categories and their associated units.

.. include:: static/units_dict.inc
