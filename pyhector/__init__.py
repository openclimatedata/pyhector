# Copyright (c) 2017-2024 pyhector authors:
#   Sven Willner <sven.willner@gmail.com>
#   Robert Gieseke <rob.g@web.de>
# Free software under GNU Affero General Public License v3, see LICENSE


"""
pyhector
--------

`pyhector` is a Python wrapper for the simple global climate
carbon-cycle model Hector (https://github.com/JGCRI/hector).

See README.rst and repository for details:
https://github.com/openclimatedata/pyhector

"""

import os
from copy import deepcopy

import numpy as np
import pandas as pd

from . import _version
from ._binding import __hector_version__  # noqa: F401  # pylint: disable=E0611
from ._binding import _Hector  # pylint: disable=no-name-in-module
from .default_config import _default_config
from .emissions import emissions
from .output import output
from .units import units

__version__ = _version.get_versions()["version"]


class Hector(_Hector):
    """Class providing an interface to Hector."""

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, type_, value, traceback):
        self.shutdown()

    def set_value(self, section, variable, value):
        """
        Set config input value directly,
        see :mod:`pyhector.emissions` for possible values.

        Parameters
        ----------
        section : str
            Component in Hector config.
        variable : str
            Name of emissions variable.
        value : pandas.Series, list, tuple, float, or str
            Pandas Series, list of tuple values with time, list of tuple values
            with time and unit, single tuple, float or string as in ini config
            file.
        """
        if isinstance(value, pd.Series):  # values with time as Series
            values = list(zip(value.index, value))
            for v in values:
                self._set_timed_double(section, variable, v[0], v[1])
        elif isinstance(value, list):  # values with time
            for v in value:
                if len(v) == 3:  # timed value with unit
                    self._set_timed_double_unit(section, variable, v[0], v[1], v[2])
                else:  # timed value without unit
                    self._set_timed_double(section, variable, v[0], v[1])
        elif isinstance(value, tuple):  # value with unit
            self._set_double_unit(section, variable, value[0], value[1])
        elif isinstance(value, str):  # value is string
            self._set_string(section, variable, value)
        else:  # value is only double
            self._set_double(section, variable, value)

    def config(self, config):
        """Set config values from config dictionary."""
        for section, data in config.items():
            for variable, value in data.items():
                self.set_value(section, variable, value)

    def set_emissions(self, scenario):
        """Set emissions from Pandas DataFrame."""
        for section in emissions:
            for source in emissions[section]:
                if source not in scenario.columns:
                    continue
                self._set_timed_array(
                    section, source, list(scenario.index), list(scenario[source])
                )


def read_hector_input(csv_file):
    """
    Reads a Hector CSV file and returns it as a Pandas DataFrame.
    """
    df = pd.read_csv(csv_file, index_col=0, comment=";")
    cols = [c for c in df.columns if "_emissions" in c or "_uptake" in c or "RF_" in c]
    df = df[cols]
    df.name = (
        os.path.splitext(os.path.basename(csv_file))[0]
        .split("_", maxsplit=1)[0]
        .upper()
    )
    return df


def write_hector_input(scenario, path=None):
    """
    Writes a scenario DataFrame to a CSV emissions file as used in Hector.

    Parameters
    ----------
    scenario : DataFrame
        DataFrame with emissions.
    path: file-like object or path

    Returns
    -------
    out : str
        If no path is given a String of the output is returned.
    """

    # Output header format:
    # ; Scenario name
    # ; Generated with pyhector
    # ;UNITS:   GtC/yr  GtC/yr [...]
    # Date      ffi_emissions   luc_emissions [...]

    out = ""
    try:
        name = "; " + scenario.name + "\n"
    except AttributeError:
        name = "; Hector Scenario\n"
    out += name

    out += "; Written with pyhector\n"
    unit_names = [units[source] for source in scenario.columns]
    out += ";UNITS:," + ",".join(unit_names) + "\n"
    out += scenario.to_csv()

    if isinstance(path, str):
        f = open(path, "w", encoding="UTF-8")
    elif path is None:
        return out
    else:
        f = path
    f.write(out)
    if hasattr(f, "close"):
        f.close()
    return None


def read_hector_constraint(constraint_file):
    """
    Reads a Hector contraint CSV file and returns it as a Pandas Series
    """
    df = pd.read_csv(constraint_file, index_col=0, comment=";")
    df = df[df.map(lambda x: isinstance(x, (int, float)))]
    df.index = df.index.astype(int)
    return df.iloc[:, 0]


def read_hector_output(csv_file):
    """
    Reads a Hector output stream CSV file and returns a wide DataFrame with
    Hector output data.
    """
    start_year = 1745
    output_stream = pd.read_csv(csv_file, comment="#")

    wide = output_stream[output_stream.year >= start_year].pivot_table(
        index="year", columns="variable", values="value"
    )

    return wide


# Default Scenarios:
ssp119 = read_hector_input(
    os.path.join(
        os.path.dirname(__file__), "./emissions/ssp119_emiss-constraints_rf.csv"
    )
)
ssp126 = read_hector_input(
    os.path.join(
        os.path.dirname(__file__), "./emissions/ssp126_emiss-constraints_rf.csv"
    )
)
ssp245 = read_hector_input(
    os.path.join(
        os.path.dirname(__file__), "./emissions/ssp245_emiss-constraints_rf.csv"
    )
)
ssp370 = read_hector_input(
    os.path.join(
        os.path.dirname(__file__), "./emissions/ssp370_emiss-constraints_rf.csv"
    )
)
ssp434 = read_hector_input(
    os.path.join(
        os.path.dirname(__file__), "./emissions/ssp434_emiss-constraints_rf.csv"
    )
)
ssp460 = read_hector_input(
    os.path.join(
        os.path.dirname(__file__), "./emissions/ssp460_emiss-constraints_rf.csv"
    )
)
ssp534_over = read_hector_input(
    os.path.join(
        os.path.dirname(__file__), "./emissions/ssp534-over_emiss-constraints_rf.csv"
    )
)
ssp585 = read_hector_input(
    os.path.join(
        os.path.dirname(__file__), "./emissions/ssp585_emiss-constraints_rf.csv"
    )
)


def run(scenario, config=None, base_config=None, outputs=None, return_config=False):
    """
    Runs a scenario through the Hector climate model.

    Parameters
    ----------
    scenario : DataFrame
        DataFrame with emissions. See ``pyhector.rcp26`` for an
        example and :mod:`pyhector.units` for units of emissions values.
    config : dictionary, default ``None``
        Additional config options that overwrite the base
        config.
    base_config : dictionary
        Base config to use. If None uses Hector's
        default config. Values in config override values in base_config.
        default None
    outputs : array_like
        List of requested output variables as strings.  if set to "all"
        returns all available variables. Defaults to global temperature,  CO2
        concentration and forcing. A full list is in :py:data:`variables`.
    return_config : boolean
        Additionaly return the full config used from adding
        ``config`` values to ``base_config``. default False

    Returns
    -------
    DataFrame
        Pandas DataFrame with results in the columns requested in ``outputs``.
    dictionary, optional
        When ``return_config`` is set to True results and
        parameters are returned as a tuple.
    """
    if outputs is None:
        outputs = [
            "temperature.global_tas",
            "simpleNbox.CO2_concentration",
            "forcing.RF_tot",
        ]
    if base_config is None:
        parameters = deepcopy(_default_config)
    else:
        parameters = deepcopy(base_config)
    if config:
        for key, data in config.items():
            for option, value in data.items():
                parameters[key][option] = value
    with Hector() as h:
        if "RF_albedo" in scenario.columns:
            parameters["simpleNbox"]["RF_albedo"] = list(
                zip(scenario["RF_albedo"].index, scenario["RF_albedo"])
            )
        h.config(parameters)
        h.set_emissions(scenario)
        if outputs == "all":
            outputs = output.keys()
        for name in outputs:
            h.add_observable(
                output[name]["component"],
                output[name]["variable"],
                output[name].get("needs_date", False),
            )
        h.run()
        results = {}
        for name in outputs:
            results[name] = h.get_observable(
                output[name]["component"], output[name]["variable"]
            )

        start = int(parameters["core"]["startDate"])
        # End of range is non-inclusive in Python ranges.
        end = int(parameters["core"]["endDate"]) + 1
        index = np.arange(start, end)
        results = pd.DataFrame(results, index=index)
    if return_config:
        return results, parameters
    return results
