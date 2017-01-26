# -*- coding: utf-8 -*-

import ctypes
import os
import pkg_resources

import numpy as np
import pandas as pd

from .default_config import default_config
from .units import units

_lib = np.ctypeslib.load_library('libpyhector', pkg_resources.resource_filename(__name__, '..'))
_lib.open.restype = ctypes.c_int
_lib.open.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
_lib.close.restype = ctypes.c_int
_lib.close.argtypes = [ctypes.c_void_p]
_lib.run.restype = ctypes.c_int
_lib.run.argtypes = [ctypes.c_void_p]
_lib.get_last_error.restype = ctypes.c_char_p
_lib.get_last_error.argtypes = None
_lib.set_value.restype = ctypes.c_int
_lib.set_value.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
_lib.set_array.restype = ctypes.c_int
_lib.set_array.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, np.ctypeslib.ndpointer(ctypes.c_int, flags='contiguous'), np.ctypeslib.ndpointer(ctypes.c_double, flags='contiguous'), ctypes.c_uint
]
_lib.add_observable.restype = ctypes.c_int
_lib.add_observable.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p
]
_lib.get_observable.restype = ctypes.c_int
_lib.get_observable.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, np.ctypeslib.ndpointer(ctypes.c_double, flags='contiguous, writeable')
]


class PyHectorException(Exception):
    pass


def _conv(v):
    return v.encode(encoding='UTF-8')

class PyHector():

    def __del__(self):
        self.close()

    def init(self):
        self.__state = ctypes.c_void_p()
        self._check(_lib.open(self.__state))

    def close(self):
        if self.__state is not None:
            _lib.close(self.__state)
            self.__state = None

    def _check(self, v):
        if v < 0:
            raise PyHectorException(_lib.get_last_error())

    def run(self):
        self.__run_size = _lib.run(self.__state)
        self._check(self.__run_size)

    def add_observable(self, component, name):
        self._check(_lib.add_observable(self.__state, _conv(component), _conv(name)))

    def get_observable(self, component, name):
        result = np.empty((self.__run_size,), dtype=np.float64)
        self._check(_lib.get_observable(self.__state, _conv(component), _conv(name), result))
        return result

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def config(self, config=None):
        parameters = default_config.copy()
        if config is not None:
            for key, data in config.items():
                for option, value in data.items():
                    parameters[key][option] = value
        for section, data in parameters.items():
            for variable, value in data.items():
                self._check(_lib.set_value(self.__state, _conv(section), _conv(variable), _conv(value)))
        return parameters


    def set_emissions(self, scenario):
        for section, variable, years, values, unit in _convert_emissions(scenario):
            self._check(
                _lib.set_array(self.__state, _conv(section), _conv(variable), years.astype(np.int32), values.astype(np.float64), len(years)))


def read_hector_input(csv_file):
    """
    Reads a Hector CSV file and returns a Pandas DataFrame.
    """
    return pd.read_csv(csv_file, skiprows=3, index_col=0)


# Default Scenarios:
rcp26 = read_hector_input(os.path.join(os.path.dirname(__file__),
    './emissions/RCP26_emissions.csv'))
rcp45 = read_hector_input(os.path.join(os.path.dirname(__file__),
    './emissions/RCP45_emissions.csv'))
rcp60 = read_hector_input(os.path.join(os.path.dirname(__file__),
    './emissions/RCP6_emissions.csv'))
rcp85 = read_hector_input(os.path.join(os.path.dirname(__file__),
    './emissions/RCP85_emissions.csv'))


# TODO Revise
def _convert_emissions(scenario):
    emissions = {
        "simpleNbox": ["anthroEmissions", "lucEmissions"],
        "so2": ["SO2_emissions"],
        "CH4": ["CH4_emissions"],
        "OH": ["NOX_emissions", "CO_emissions", "NMVOC_emissions"],
        "ozone": ["NOX_emissions", "CO_emissions", "NMVOC_emissions"],
        "N2O": ["N2O_emissions"],
        "bc": ["BC_emissions"],
        "oc": ["OC_emissions"],
        "CF4_halocarbon": ["CF4_emissions"],
        "C2F6_halocarbon": ["C2F6_emissions"],
        "C4F10_halocarbon": ["C4F10_emissions"],  # commented out in RCP
        "HFC23_halocarbon": ["HFC23_emissions"],
        "HFC32_halocarbon": ["HFC32_emissions"],
        "HFC4310_halocarbon": ["HFC4310_emissions"],
        "HFC125_halocarbon": ["HFC125_emissions"],
        "HFC134a_halocarbon": ["HFC134a_emissions"],
        "HFC143a_halocarbon": ["HFC143a_emissions"],
        "HFC152a_halocarbon": ["HFC152a_emissions"],  # commented out in RCP
        "HFC227ea_halocarbon": ["HFC227ea_emissions"],
        "HFC245fa_halocarbon": ["HFC245fa_emissions"],
        "HFC236fa_halocarbon": ["HFC236fa_emissions"],  # commented out in RCP
        "SF6_halocarbon": ["SF6_emissions"],
        "CFC11_halocarbon": ["CFC11_emissions"],
        "CFC12_halocarbon": ["CFC12_emissions"],
        "CFC113_halocarbon": ["CFC113_emissions"],
        "CFC114_halocarbon": ["CFC114_emissions"],
        "CFC115_halocarbon": ["CFC115_emissions"],
        "CCl4_halocarbon": ["CCl4_emissions"],
        "CH3CCl3_halocarbon": ["CH3CCl3_emissions"],
        "halon1211_halocarbon": ["halon1211_emissions"],
        "halon1301_halocarbon": ["halon1301_emissions"],
        "halon2402_halocarbon": ["halon2402_emissions"],
        "HCF22_halocarbon": ["HCF22_emissions"],
        "HCF141b_halocarbon": ["HCF141b_emissions"],
        "HCF142b_halocarbon": ["HCF142b_emissions"],
        "HCF143_halocarbon": ["HCF143_emissions"],  # commented out in RCP
        "CH3Cl_halocarbon": ["CH3Cl_emissions"],
        "CH3Br_halocarbon": ["CH3Br_emissions"]
    }
    # List of tuples [("so2", "SO2_emissions", [... array ], unit), ...]
    output = []
    for category in emissions:
        for source in emissions[category]:
            if source in scenario:
                gas = scenario[source]
                output.append((
                  category,
                  source,
                  np.array(gas.index),
                  np.array(gas),
                  units[source],
                ))
    return output


def run(scenario, config_options=None):
    """
    TODO
    """
    with PyHector() as h:
        parameters = h.config(config_options)
        h.set_emissions(scenario)
        h.add_observable("temperature", "Tgav")
        h.run()
        global_temp = h.get_observable("temperature", "Tgav")
        start = int(parameters["core"]["startDate"])
        end = int(parameters["core"]["endDate"])
    return pd.Series(global_temp, index=np.arange(start, end))
