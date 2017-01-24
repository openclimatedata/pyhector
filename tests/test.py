#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import sys, path
sys.path = [path.dirname(path.dirname(path.abspath(__file__)))] + sys.path
from pyhector import *

# TODO Useful for comparing pyhector output with original Hector streams.
def read_hector_output(csv_file, start_year=1750):
    """
    Reads a Hector output stream csv and returns a wide DataFrame with
    Hector output data.

    TODO
    doc param
    """

    output_stream = pd.read_csv(csv_file, skiprows=1)

    wide = output_stream[output_stream.year >= start_year].pivot_table(
        index="year", columns="variable", values="value")

    return wide



with PyHector() as h:
    h.config()
    h.set_emissions(rcp26)
    h.add_observable("temperature", "Tgav")
    h.run()
    print(h.get_observable("temperature", "Tgav"))
