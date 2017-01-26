#!/usr/bin/env python3

# Save Hector default config and emissions units as importable Python
# modules.
# Usage (requires Pandas):
# Run this script as
#   ./write_defaults.py

import configparser
import os

import pandas as pd

from pprint import pformat


# Default config from `ini`-file
default_config = os.path.join(os.path.dirname(__file__),
                              '../pyhector/rcp_default.ini')
config = configparser.ConfigParser(inline_comment_prefixes=(';'))
config.optionxform = str
config.read(default_config)

parameters = {}
for section in config.sections():
    parameters[section] = {}
    for option in config.options(section):
        parameters[section][option] = config.get(section, option)

output = "default_config = {\n    " + \
         pformat(parameters, indent=1, width=1)[1:-1].replace(
            "\n '", "\n    '").replace(
            "     '", "        '") + \
            "\n}\n"
with open(os.path.join(os.path.dirname(__file__),
          '../pyhector/default_config.py'), 'w') as f:
    f.write(output)

# Default units from input CSV
units = pd.read_csv(
    os.path.join(os.path.dirname(__file__),
        '../pyhector/emissions/RCP26_emissions.csv'),
    skiprows=2,
    header=None)
units = units.loc[:1, 1:].T.set_index(1).to_dict()[0]
with open(os.path.join(os.path.dirname(__file__),
          "../pyhector/units.py"), "w") as f:
    f.write("units = {\n ")
    f.write(pformat(units, indent=4)[1:-1])
    f.write("\n}\n")
