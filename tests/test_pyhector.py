# -*- coding: utf-8 -*-

import os
from copy import deepcopy

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

import pyhector
from pyhector import (
    Hector,
    constants,
    ssp119,
    ssp126,
    ssp245,
    ssp370,
    ssp434,
    ssp460,
    ssp534_over,
    ssp585,
    read_hector_constraint,
    read_hector_input,
    read_hector_output,
    write_hector_input,
)
from pyhector.output import output

path = os.path.dirname(__file__)
ssps = {
    "ssp119": ssp119,
    "ssp126": ssp126,
    "ssp245": ssp245,
    "ssp370": ssp370,
    "ssp434": ssp434,
    "ssp460": ssp460,
    "ssp534-over": ssp534_over,
    "ssp585": ssp585,
}


def test_constants():
    assert constants


def test_read_hector_input():
    ssp126 = read_hector_input(
        os.path.join(
            os.path.dirname(__file__),
            "../pyhector/emissions/ssp126_emiss-constraints_rf.csv",
        )
    )
    assert isinstance(ssp126, pd.DataFrame)
    assert ssp126.index[-1] == 2300
    assert ssp126.name == "SSP126"
    assert "daccs_uptake" in ssp126.columns
    assert "ffi_emissions" in ssp126.columns
    assert "CO2_constrain" not in ssp126.columns


def test_write_hector_input(tmpdir):
    testfile = tmpdir.join("test.csv")
    write_hector_input(ssp126, testfile)
    print(testfile.read())
    scen_ssp126 = read_hector_input(str(testfile))
    assert_frame_equal(ssp126, scen_ssp126)


def test_ssps():
    # Compare output of Pyhector with original Hector output streams for SSPs.
    for name, scenario in ssps.items():
        original = read_hector_output(
            os.path.join(path, "./data/outputstream_{}.csv".format(name))
        )
        output = pyhector.run(scenario)
        assert_series_equal(
            output["temperature.global_tas"],
            original.global_tas,
            check_names=False,
            check_exact=False,
            rtol=3,
        )


def test_default_options():
    # Original dictionary with default options should remain unchanged.
    assert pyhector._default_config["core"]["endDate"] == 2300
    pyhector.run(ssp126, {"core": {"endDate": 2100}})
    assert pyhector._default_config["core"]["endDate"] == 2300


def test_units():
    assert pyhector.units["ffi_emissions"] == "GtC/yr"
    assert pyhector.units["luc_emissions"] == "GtC/yr"
    assert pyhector.units["NOX_emissions"] == "MtN/yr"


def test_output_variables():
    results = pyhector.run(ssp126)
    assert len(results.columns) == 3
    results = pyhector.run(ssp126, outputs="all")
    assert len(results.columns) == len(pyhector.output.keys())


def test_output_variables_needs_date():
    # Some outputs require the "needs_date" flag to be set to True.
    needing_date = ["CH4.CH4_concentration", "N2O.N2O_concentration", "OH.TAU_OH", "ozone.O3_concentration"]
    results = pyhector.run(ssp126, outputs=needing_date)
    assert list(results.columns) == needing_date


def test_use_base_config():
    results, params = pyhector.run(
        ssp126, base_config=pyhector._default_config, return_config=True
    )
    assert params == pyhector._default_config


def test_reading_constraint_file():
    lawdome_co2_csv = os.path.join(path, "data/lawdome_co2.csv")
    lawdome = read_hector_constraint(lawdome_co2_csv)
    assert lawdome.loc[1010] == 279.5
    assert lawdome.loc[2008] == 385.34


# Tests following Hector's `test_hector.sh` script
# Make sure the model handles year changes
def test_year_changes():
    results = pyhector.run(ssp245, {"core": {"startDate": 1745}})
    assert results.index[0] == 1745
    results = pyhector.run(ssp245, {"core": {"endDate": 2250}})
    assert results.index[-1] == 2250


# Spinup output
def test_spinup_output():
    parameters = deepcopy(pyhector._default_config)
    with Hector() as h:
        h.config(parameters)
        h.set_emissions(ssp245)
        name = "simpleNbox.CO2_concentration"
        h.add_observable(
            output[name]["component"],
            output[name]["variable"],
            output[name].get("needs_date", True),
            in_spinup=True,
        )
        h.run()
        results = h.get_observable(
            output[name]["component"], output[name]["variable"], in_spinup=True
        )
        assert h.spinup_size == len(results)


# Turn off spinup
def test_turn_off_spinup():
    parameters = deepcopy(pyhector._default_config)
    with Hector() as h:
        h.config(parameters)
        h.set_emissions(ssp245)
        h.run()
        assert h.spinup_size > 0
    with Hector() as h:
        parameters["core"]["do_spinup"] = False
        h.config(parameters)
        h.set_emissions(ssp245)
        h.run()
        assert h.spinup_size == 0


# Turn on the constraint settings one by one and run the model
# CO2
def test_constraint_co2():
    lawdome_co2_csv = os.path.join(path, "data/lawdome_co2.csv")
    lawdome_co2 = read_hector_constraint(lawdome_co2_csv)
    output = pyhector.run(ssp245, {"simpleNbox": {"CO2_constrain": lawdome_co2}})
    # Simplifying the overlapping date-range (later CO2 values are yearly.)
    assert_series_equal(
        output["simpleNbox.CO2_concentration"].loc[1750:1960:5],
        lawdome_co2.loc[1750:1960],
        check_names=False,
    )


# Radiative forcing
def test_constraint_forcing():
    forcing_csv = os.path.join(path, "data/MAGICC_RF_4.5.csv")
    forcing = read_hector_constraint(forcing_csv)
    output = pyhector.run(ssp245, {"forcing": {"RF_tot_constrain": forcing}})
    assert_series_equal(
        output["forcing.RF_tot"].loc[1765:2300], forcing.loc[1765:2300], check_names=False
    )


# Ensure that Hector version and Pyhector version match
def test_hector_version():
    if "+" in pyhector.__version__:
        pass
    else:
        assert (
            ".".join(pyhector.__version__.split(".")[:3]) == pyhector.__hector_version__
        )
