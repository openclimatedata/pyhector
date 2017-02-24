# -*- coding: utf-8 -*-

import os

import pandas as pd
import pytest

from pandas.util.testing import assert_series_equal

import pyhector
from pyhector import (
    Hector, rcp26, rcp45, rcp60, rcp85, read_hector_input, read_hector_output
)


path = os.path.dirname(__file__)
rcps = {
    'rcp26': rcp26,
    'rcp45': rcp45,
    'rcp60': rcp60,
    'rcp85': rcp85
}


def test_read_hector_input():
    rcp26 = read_hector_input(
        os.path.join(os.path.dirname(__file__),
        '../pyhector/emissions/RCP26_emissions.csv')
    )
    assert isinstance(rcp26, pd.DataFrame)
    assert rcp26.index[-1] == 2500
    assert rcp26.name == "RCP26_emissions"


def test_rcps():
    # Compare output of Pyhector with original Hector output streams for RCPs.
    for name, scenario in rcps.items():
        original = read_hector_output(
            os.path.join(path, "./data/outputstream_{}.csv".format(name))
        )
        output = pyhector.run(scenario)
        assert_series_equal(
            output["temperature.Tgav"], original.Tgav, check_names=False)


def test_default_options():
    with Hector() as h:
        parameters = h.config()
    assert parameters["core"]["endDate"] == 2300


def test_default_options():
    assert pyhector._default_config["core"]["endDate"] == 2300
    pyhector.run(rcp26, {"core": {"endDate": 2100}})
    assert pyhector._default_config["core"]["endDate"] == 2300


def test_units():
    assert pyhector.units["anthroEmissions"] == 'GtC/yr'
    assert pyhector.units["lucEmissions"] == 'GtC/yr'
    assert pyhector.units["NOX_emissions"] == 'MtN/yr'


def test_output_variables():
    results = pyhector.run(rcp26)
    assert len(results.columns) == 3
    results = pyhector.run(rcp26, outputs="all")
    assert len(results.columns) == len(pyhector.variables.keys())


def test_output_variables_needs_date():
    # Some outputs require the "needs_date" flag to be set to True.
    needing_date = ["CH4.CH4", "N2O.N2O", "OH.TAU_OH", "ozone.O3"]
    results = pyhector.run(rcp26, outputs=needing_date)
    assert list(results.columns) == needing_date


def test_use_base_config():
    results, params = pyhector.run(
        rcp26,  base_config=pyhector._default_config, return_config=True)
    assert params == pyhector._default_config


# Tests following Hector's `test_hector.sh` script
# Make sure the model handles year changes
def test_year_changes():
    results = pyhector.run(rcp45, {"core": {"startDate": 1745}})
    # Output dates are reported as end of simulation year (1745-12-31 = 1746.0)
    assert results.index[0] == 1746
    results = pyhector.run(rcp45, {"core": {"endDate": 2250}})
    assert results.index[-1] == 2250

# Turn off spinup
@pytest.mark.skip(reason="no way of currently testing this")
def test_turn_off_spinup():
    results = pyhector.run(rcp45, {"core": {"do_spinup": False}})
    # Spin-up output seems to be not available in pyhector

# Turn on the constraint settings one by one and run the model
# CO2
def test_contraint_setting():
    lawdome_co2_csv = os.path.join(path, "data/lawdome_co2.csv")
    lawdome_co2 = pd.read_csv(lawdome_co2_csv,
        skiprows=[0, 1, 3], index_col=0, comment=";")
    lawdome_co2.index = lawdome_co2.index.astype(int)
    values = list(zip(lawdome_co2.index, lawdome_co2.Ca_constrain,))
    output = pyhector.run(rcp45,
        {"simpleNbox": {"Ca_constrain": values}})
    # Simplifying the overlapping date-range (later lawdome values are yearly.)
    assert_series_equal(
        output["simpleNbox.Ca"].loc[1750:1960:5],
        lawdome_co2.Ca_constrain.loc[1750:1960], check_names=False)


