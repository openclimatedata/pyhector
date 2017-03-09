# Copyright (c) 2017 pyhector authors:
#   Sven Willner <sven.willner@pik-potsdam.de>
#   Robert Gieseke <robert.gieseke@pik-potsdam.de>
# Free software under GNU Affero General Public License v3, see LICENSE

# -*- coding: utf-8 -*-

"""
pyhector
--------

`pyhector` is a Python wrapper for the simple global climate
carbon-cycle model Hector (https://github.com/JGCRI/hector).

See README.md and repository for details:
https://github.com/openclimatedata/pyhector

"""

import ctypes
import os
import pkg_resources

import numpy as np
import pandas as pd

from copy import deepcopy

from .default_config import _default_config
from .units import units  # NOQA
from .emissions import emissions
from .output import variables

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


_lib = np.ctypeslib.load_library(
    'libpyhector',
    pkg_resources.resource_filename(__name__, '..')
)
_lib.hector_open.restype = ctypes.c_int
_lib.hector_open.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
_lib.hector_close.restype = ctypes.c_int
_lib.hector_close.argtypes = [ctypes.c_void_p]
_lib.hector_run.restype = ctypes.c_int
_lib.hector_run.argtypes = [ctypes.c_void_p]
_lib.hector_get_last_error.restype = ctypes.c_char_p
_lib.hector_get_last_error.argtypes = None
_lib.hector_set_value_string.restype = ctypes.c_int
_lib.hector_set_value_string.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
]
_lib.hector_set_value.restype = ctypes.c_int
_lib.hector_set_value.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double
]
_lib.hector_set_value_unit.restype = ctypes.c_int
_lib.hector_set_value_unit.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double,
    ctypes.c_char_p
]
_lib.hector_set_timed_value.restype = ctypes.c_int
_lib.hector_set_timed_value.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
    ctypes.c_double
]
_lib.hector_set_timed_value_unit.restype = ctypes.c_int
_lib.hector_set_timed_value_unit.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
    ctypes.c_double, ctypes.c_char_p
]
_lib.hector_set_array.restype = ctypes.c_int
_lib.hector_set_array.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    np.ctypeslib.ndpointer(ctypes.c_int, flags='contiguous'),
    np.ctypeslib.ndpointer(ctypes.c_double, flags='contiguous'),
    ctypes.c_uint
]
_lib.hector_add_observable.restype = ctypes.c_int
_lib.hector_add_observable.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_bool
]
_lib.hector_get_observable.restype = ctypes.c_int
_lib.hector_get_observable.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    np.ctypeslib.ndpointer(ctypes.c_double, flags='contiguous, writeable')
]


class HectorException(Exception):
    """Wrapper for Hector Exception."""
    pass


def _conv(v):
    return str(v).encode(encoding='UTF-8')


class Hector():
    """Class providing an interface to Hector."""

    def __del__(self):
        self.close()

    def init(self):
        """Initialise a Hector instance."""
        self.__state = ctypes.c_void_p()
        self._check(_lib.hector_open(self.__state))

    def close(self):
        """Close Hector instance."""
        if self.__state is not None:
            _lib.hector_close(self.__state)
            self.__state = None

    def _check(self, v):
        if v < 0:
            raise HectorException(_lib.hector_get_last_error())

    def run(self):
        """Run Hector."""
        self.__run_size = _lib.hector_run(self.__state)
        self._check(self.__run_size)

    def add_observable(self, component, name, needs_date=False):
        """
        Add variable that can be read later.
        See :mod:`pyhector.output` for available variables.
        """
        self._check(_lib.hector_add_observable(
            self.__state, _conv(component), _conv(name), needs_date)
        )

    def get_observable(self, component, name):
        """
        Returns output variable.
        See :mod:`pyhector.output` for available variables.
        """
        result = np.empty((self.__run_size,), dtype=np.float64)
        self._check(_lib.hector_get_observable(
            self.__state, _conv(component), _conv(name), result)
        )
        return result

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def set_value(self, section, variable, value):
        """
        Set config input value directly,
        see :mod:`pyhector.emissions` for possible values.

        Parameters
        ----------
        section: str
            Component in Hector config.
        variable: str
            Name of emissions variable.
        value: pandas.Series, list, tuple, float, or str
            Pandas Series, list of tuple values with time, list of tuple values
            with time and unit, single tuple, float or string as in ini config
            file.

        """
        if isinstance(value, pd.Series):  # values with time as Series
            values = list(zip(value.index, value))
            for v in values:
                self._check(_lib.hector_set_timed_value(
                    self.__state, _conv(section), _conv(variable),
                    v[0], v[1]))
        elif isinstance(value, list):  # values with time
            for v in value:
                if len(v) == 3:  # timed value with unit
                    self._check(_lib.hector_set_value(
                        self.__state, _conv(section), _conv(variable), v[0],
                        v[1], v[2]))
                else:  # timed value without unit
                    self._check(_lib.hector_set_timed_value(
                        self.__state, _conv(section), _conv(variable),
                        v[0], v[1]))
        elif isinstance(value, tuple):  # value with unit
            self._check(_lib.hector_set_value_unit(
                        self.__state, _conv(section), _conv(variable),
                        value[0], _conv(value[1])))
        elif isinstance(value, str):  # value is string
            self._check(_lib.hector_set_value_string(
                self.__state, _conv(section), _conv(variable), _conv(value)))
        else:  # value is only double
            self._check(_lib.hector_set_value(self.__state, _conv(section),
                                              _conv(variable), value))

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
                years = np.array(scenario.index, dtype=np.int32)
                values = np.array(scenario[source], dtype=np.float64)
                self._check(
                    _lib.hector_set_array(
                        self.__state,
                        _conv(section),
                        _conv(source),
                        years,
                        values,
                        len(years))
                    )


def read_hector_input(csv_file):
    """
    Reads a Hector CSV file and returns it as a Pandas DataFrame.
    """
    df = pd.read_csv(csv_file, skiprows=3, index_col=0)
    df.name = os.path.splitext(os.path.basename(csv_file))[0]
    return df


def read_hector_constraint(constraint_file):
    """
    Reads a Hector contraint CSV file and returns it as a Pandas Series
    """
    df = pd.read_csv(constraint_file, index_col=0, comment=";")
    df = df[df.applymap(lambda x: isinstance(x, (int, float)))]
    df.index = df.index.astype(int)
    return df.ix[:, 0]


def read_hector_output(csv_file):
    """
    Reads a Hector output stream CSV file and returns a wide DataFrame with
    Hector output data.
    """
    # Filter out spin-up values. In Hector 1.x RCP output streams years are
    # given as end of simulation year.
    # See https://github.com/JGCRI/hector/issues/177
    start_year = 1746
    output_stream = pd.read_csv(csv_file, skiprows=1)

    wide = output_stream[output_stream.year >= start_year].pivot_table(
        index="year", columns="variable", values="value")

    return wide


# Default Scenarios:
rcp26 = read_hector_input(
    os.path.join(os.path.dirname(__file__), './emissions/RCP26_emissions.csv')
)
rcp45 = read_hector_input(
    os.path.join(os.path.dirname(__file__), './emissions/RCP45_emissions.csv')
)
rcp60 = read_hector_input(
    os.path.join(os.path.dirname(__file__), './emissions/RCP6_emissions.csv')
)
rcp85 = read_hector_input(
    os.path.join(os.path.dirname(__file__), './emissions/RCP85_emissions.csv')
)


def run(scenario, config=None, base_config=None,
        outputs=['temperature.Tgav', 'simpleNbox.Ca', 'forcing.Ftot'],
        return_config=False):
    """
    Runs a scenario through the Hector climate model.

    Parameters
    ----------
    scenario: DataFrame
        DataFrame with emissions. See ``pyhector.rcp26`` for an
        example and pyhector.units for units of emissions values.
    config: dictionary
        Additional config options that overwrite the base
        config. default None
    base_config: dictionary
        Base config to use. If None uses Hector's
        default config. Values in config override values in base_config.
        default None
    outputs: array_like
        List of requested output variables as strings.  if set to "all"
        returns all available variables. Defaults to global temperature,  CO2
        concentration and forcing. A full list is in ``pyhector.variables``.
    return_config: boolean
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
    if base_config is None:
        parameters = deepcopy(_default_config)
    else:
        parameters = deepcopy(base_config)
    if config:
        for key, data in config.items():
            for option, value in data.items():
                parameters[key][option] = value
    with Hector() as h:
        h.config(parameters)
        h.set_emissions(scenario)
        if outputs == "all":
            outputs = variables.keys()
        for name in outputs:
            h.add_observable(variables[name]["component"],
                             variables[name]["variable"],
                             variables[name].get("needs_date", False))
        h.run()
        results = {}
        for name in outputs:
            results[name] = h.get_observable(
                variables[name]["component"], variables[name]["variable"])

        # In Hector 1.x output value years are given as end of simulation
        # year, e.g. 1745-12-31 = 1746.0.
        # See https://github.com/JGCRI/hector/issues/177
        start = int(parameters["core"]["startDate"]) + 1
        # End of range is non-inclusive in Python ranges.
        end = int(parameters["core"]["endDate"]) + 1
        index = np.arange(start, end)
        results = pd.DataFrame(results, index=index)
    if return_config:
        return results, parameters
    else:
        return results
