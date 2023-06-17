# -*- coding: utf-8 -*-

import os
from copy import deepcopy

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

import pyhector
from pyhector import (
    Hector,
    constants,
    rcp26,
    rcp45,
    rcp60,
    rcp85,
    read_hector_constraint,
    read_hector_input,
    read_hector_output,
    write_hector_input,
)
from pyhector.output import output

path = os.path.dirname(__file__)
rcps = {"rcp26": rcp26, "rcp45": rcp45, "rcp60": rcp60, "rcp85": rcp85}


def test_constants():
    assert constants


def test_read_hector_input():
    rcp26 = read_hector_input(
        os.path.join(
            os.path.dirname(__file__), "../pyhector/emissions/RCP26_emissions.csv"
        )
    )
    assert isinstance(rcp26, pd.DataFrame)
    assert rcp26.index[-1] == 2500
    assert rcp26.name == "RCP26_emissions"


def test_write_hector_input(tmpdir):
    testfile = tmpdir.join("test.csv")
    write_hector_input(rcp26, testfile)
    print(testfile.read())
    scen_rcp26 = read_hector_input(str(testfile))
    assert_frame_equal(rcp26, scen_rcp26)


def test_rcps():
    # Compare output of Pyhector with original Hector output streams for RCPs.
    for name, scenario in rcps.items():
        original = read_hector_output(
            os.path.join(path, "./data/outputstream_{}.csv".format(name))
        )
        output = pyhector.run(scenario)
        assert_series_equal(
            output["temperature.Tgav"],
            original.Tgav,
            check_names=False,
            check_exact=False,
            rtol=3
        )


def test_default_options():
    assert pyhector._default_config["core"]["endDate"] == 2300
    pyhector.run(rcp26, {"core": {"endDate": 2100}})
    assert pyhector._default_config["core"]["endDate"] == 2300


def test_units():
    assert pyhector.units["ffi_emissions"] == "GtC/yr"
    assert pyhector.units["luc_emissions"] == "GtC/yr"
    assert pyhector.units["NOX_emissions"] == "MtN/yr"


def test_output_variables():
    results = pyhector.run(rcp26)
    assert len(results.columns) == 3
    results = pyhector.run(rcp26, outputs="all")
    assert len(results.columns) == len(pyhector.output.keys())


def test_output_variables_needs_date():
    # Some outputs require the "needs_date" flag to be set to True.
    needing_date = ["CH4.CH4", "N2O.N2O", "OH.TAU_OH", "ozone.O3"]
    results = pyhector.run(rcp26, outputs=needing_date)
    assert list(results.columns) == needing_date


def test_use_base_config():
    results, params = pyhector.run(
        rcp26, base_config=pyhector._default_config, return_config=True
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
    results = pyhector.run(rcp45, {"core": {"startDate": 1745}})
    # Output dates are reported as end of simulation year (1745-12-31 = 1746.0)
    assert results.index[0] == 1746
    results = pyhector.run(rcp45, {"core": {"endDate": 2250}})
    assert results.index[-1] == 2250


# Spinup output
def test_spinup_output():
    parameters = deepcopy(pyhector._default_config)
    with Hector() as h:
        h.config(parameters)
        h.set_emissions(rcp45)
        name = "simpleNbox.Ca"
        h.add_observable(
            output[name]["component"],
            output[name]["variable"],
            output[name].get("needs_date", False),
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
        h.set_emissions(rcp45)
        h.run()
        assert h.spinup_size > 0
    with Hector() as h:
        parameters["core"]["do_spinup"] = False
        h.config(parameters)
        h.set_emissions(rcp45)
        h.run()
        assert h.spinup_size == 0


# Turn on the constraint settings one by one and run the model
# CO2
def test_constraint_co2():
    lawdome_co2_csv = os.path.join(path, "data/lawdome_co2.csv")
    lawdome_co2 = read_hector_constraint(lawdome_co2_csv)
    output = pyhector.run(rcp45, {"simpleNbox": {"Ca_constrain": lawdome_co2}})
    # Simplifying the overlapping date-range (later CO2 values are yearly.)
    assert_series_equal(
        output["simpleNbox.Ca"].loc[1750:1960:5],
        lawdome_co2.loc[1750:1960],
        check_names=False,
    )


# Radiative forcing
def test_constraint_forcing():
    forcing_csv = os.path.join(path, "data/MAGICC_RF_4.5.csv")
    forcing = read_hector_constraint(forcing_csv)
    output = pyhector.run(rcp45, {"forcing": {"Ftot_constrain": forcing}})
    assert_series_equal(
        output["forcing.Ftot"].loc[1765:2300], forcing.loc[1765:2300], check_names=False
    )


# Ensure that Hector version and Pyhector version match
def test_hector_version():
    if "+" in pyhector.__version__:
        pass
    else:
        assert (
            ".".join(pyhector.__version__.split(".")[:3]) == pyhector.__hector_version__
        )
