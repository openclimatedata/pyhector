#!/usr/bin/env python3

# Save Hector default config and emissions units as importable Python
# modules.
# Usage (requires Pandas):
# Run this script as
#   ./write_defaults.py

import ast
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

output = '"""Dictionary with default config."""\n\n'

parameters = {}
for section in config.sections():
    if len(config.options(section)) > 0:
        parameters[section] = {}
        for option in config.options(section):
            value = config.get(section, option)
            # Hector-specific ini property-value assignment with time index,
            # like 'Ftalbedo[1750]' will be turned into a list of tuples.
            if option.endswith("]"):
                split = option.split("[")
                name = split[0]
                year = int(split[1][:-1])  # leave out closing "]"
                if name not in parameters[section]:
                    parameters[section][name] = []
                parameters[section][name].append(
                    (year, ast.literal_eval(value),)
                )
            else:
                if option == 'run_name':
                    value = "pyhector-run"
                elif option in ["enabled", "do_spinup"]:
                    value = True if 1 else False
                # Values containing a unit like "H0=35.0,pptv" are split and
                # turned into a tuple.
                elif "," in value:
                    number, unit = tuple(value.split(","))
                    value = (ast.literal_eval(number), unit,)
                # Convert floats and ints to Python numbers
                else:
                    value = ast.literal_eval(value)
                parameters[section][option] = value

output += "_default_config = {\n    " + \
         pformat(parameters, indent=1, width=75)[1:-1].replace(
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
    f.write('"""')
    f.write('Dictionary of emissions and their expected units in Hector.')
    f.write('"""\n\n')
    f.write("units = {\n ")
    f.write(pformat(units, indent=4)[1:-1])
    f.write("\n}\n")
