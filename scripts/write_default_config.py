#!/usr/bin/env python3

# Save Hector default config as a Python dictionary.
# Usage:
# Run this script as
#   ./write_default_config.py

import configparser
import os

from pprint import pformat


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
