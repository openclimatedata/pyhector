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
    from tabulate import tabulate
    print(tabulate(map(lambda item: ("``%s``" % item[0],
                                     ", ".join(map(lambda i: "``%s``" % i, item[1]))),
                       sorted(emissions.items())),
                   ["component", "emissions"],
                   tablefmt="grid"))

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

.. exec::
    from pyhector import output
    from tabulate import tabulate
    sorted_output = sorted(output.items(),
                              key=output.get("component"))
    print(tabulate(map(lambda item: ("``%s``" % item[1]["component"],
                                     "``%s``" % item[1]["variable"],
                                     item[1]["description"],
                                     "``%s``" % item[1]["unit"]),
                       sorted_output),
                   ["component", "variable", "description", "unit"],
                   tablefmt="grid"))

pyhector.units
--------------

A dictionary with emissions categories and their associated units.

.. exec::
    from pyhector import units
    from tabulate import tabulate
    print(tabulate(map(lambda item: ("``%s``" % item[0],
                                     "``%s``" % item[1]),
                       sorted(units.items())),
                   ["emissions", "unit"],
                   tablefmt="grid"))
