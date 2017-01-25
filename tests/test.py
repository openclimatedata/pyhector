# -*- coding: utf-8 -*-

import os

import pandas as pd

import pyhector
from pyhector import rcp26, rcp45, rcp60, rcp85


path = os.path.dirname(__file__)
rcps = {
    'rcp26': rcp26,
    'rcp45': rcp45,
    'rcp60': rcp60,
    'rcp85': rcp85
}


def read_hector_output(csv_file):
    """
    Reads a Hector output stream csv and returns a wide DataFrame with
    Hector output data.
    """
    # Filter out spin-up values. RCP output streams seem to start at 1746
    # though startDate ist 1745.
    start_year = 1746
    output_stream = pd.read_csv(csv_file, skiprows=1)

    wide = output_stream[output_stream.year >= start_year].pivot_table(
        index="year", columns="variable", values="value")

    return wide


def test_rcps():
    # Compare output of Pyhector with original Hector output streams for RCPs.
    for name, scenario in rcps.items():
        original = read_hector_output(
            os.path.join(path, "./data/outputstream_{}.csv".format(name))
        )
        output = pyhector.run(scenario)
        assert output.loc[1746:].round(2).equals(original.Tgav.round(2))
