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

.. exec::
    from pyhector import emissions
    sorted_emissions = sorted(emissions.items())
    for item in sorted_emissions:
        print("- ``{}``: {}".format(item[0], item[1]))
pyhector.output
---------------

A dictionary with Hector's available output variables

    output = {
        'C2F6_halocarbon.hc_concentration': {
            'component': 'C2F6_halocarbon',
            'description': 'C2F6 concentration',
            'unit': 'pptv',
            'variable': 'hc_concentration'
        },
        [...]

Full list below, sorted by dictionary key "component.variable", showing
description and the associated unit:

.. exec::
    from pyhector import variables
    template = "- ``{}.{}``, {}, {}"
    sorted_variables = sorted(variables.items(),
                              key=variables.get("component"))
    for item in sorted_variables:
        print(template.format(
            item[1]["component"],
            item[1]["variable"],
            item[1]["description"],
            item[1]["unit"]))

pyhector.units
--------------

A dictionary with emissions categories and their associated units.

.. exec::
    from pyhector import units
    for key, value in sorted(units.items()):
        print("- ``{}``:  {}\n".format(key, value))
