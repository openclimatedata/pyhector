# -*- coding: utf-8 -*-

import configparser
import ctypes
import os
import pkg_resources

import numpy as np
import pandas as pd


_lib = np.ctypeslib.load_library('libpyhector', pkg_resources.resource_filename(__name__, '..'))
_lib.open.restype = ctypes.c_int
_lib.open.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
_lib.close.restype = ctypes.c_int
_lib.close.argtypes = [ctypes.c_void_p]
_lib.run.restype = ctypes.c_int
_lib.run.argtypes = [ctypes.c_void_p]
_lib.get_last_error.restype = ctypes.c_char_p
_lib.get_last_error.argtypes = None
_lib.set_config_value.restype = ctypes.c_int
_lib.set_config_value.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
_lib.set_config_timed_value.restype = ctypes.c_int
_lib.set_config_timed_value.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p
]
_lib.set_emissions.restype = ctypes.c_int
_lib.set_emissions.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_double
]
_lib.set_emissions_array.restype = ctypes.c_int
_lib.set_emissions_array.argtypes = [
    ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, np.ctypeslib.ndpointer(
        ctypes.c_double, ndim=2, flags='contiguous'), ctypes.c_uint
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

    __STATE_BEGIN = 0
    __STATE_INITIALIZED = 1
    __STATE_CONFIGURED = 2
    __STATE_HAS_RUN = 3

    def __init__(self):
        self.__state_id = self.__STATE_BEGIN

    def __del__(self):
        self.close()

    def init(self):
        self._check_state(at_least=self.__STATE_BEGIN, before=self.__STATE_INITIALIZED)
        self.__state = ctypes.c_void_p()
        self._check(_lib.open(self.__state))
        self.__state_id = self.__STATE_INITIALIZED

    def close(self):
        if self.__state_id >= self.__STATE_INITIALIZED:
            _lib.close(self.__state)
            self.__state_id = self.__STATE_BEGIN

    def _check(self, v):
        if v < 0:
            if v == -1:
                raise PyHectorException(_lib.get_last_error())
            else:
                raise Exception(_lib.get_last_error())

    def _check_state(self, at_least=None, before=None):
        if at_least is not None and self.__state_id < at_least:
            if at_least == self.__STATE_INITIALIZED:
                raise Exception("Not initialized yet")
            elif at_least == self.__STATE_CONFIGURED:
                raise Exception("Not configured yet")
            elif at_least == self.__STATE_HAS_RUN:
                raise Exception("Has not run yet")
        elif before is not None and self.__state_id >= before:
            if before == self.__STATE_INITIALIZED:
                raise Exception("Already initialized")
            elif before == self.__STATE_CONFIGURED:
                raise Exception("Already configured")
            elif before == self.__STATE_HAS_RUN:
                raise Exception("Has already run")

    def run(self):
        self._check_state(at_least=self.__STATE_CONFIGURED)
        self.__run_size = _lib.run(self.__state)
        self._check(self.__run_size)
        self.__state_id = self.__STATE_HAS_RUN

    def add_observable(self, component, name):
        self._check_state(at_least=self.__STATE_CONFIGURED)
        self._check(_lib.add_observable(self.__state, _conv(component), _conv(name)))

    def get_observable(self, component, name):
        self._check_state(at_least=self.__STATE_HAS_RUN)
        result = np.empty((self.__run_size,), dtype=np.float64)
        self._check(_lib.get_observable(self.__state, _conv(component), _conv(name), result))
        return result

    def __enter__(self):
        self.init()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def config(self, config=None):
        self._check_state(at_least=self.__STATE_INITIALIZED)
        conf = _read_default_config()
        if config is not None:
            conf.update(config)
        for section, data in conf.items():
            for variable, value in data.items():
                if "[" in variable:
                    variable = variable.split("[")
                    self._check(
                        _lib.set_config_timed_value(self.__state, _conv(section), _conv(variable[0]), float(variable[1][:-1]), _conv(value)))
                else:
                    self._check(_lib.set_config_value(self.__state, _conv(section), _conv(variable), _conv(value)))
        self.__state_id = self.__STATE_CONFIGURED

    def set_emissions(self, scenario):
        self._check_state(at_least=self.__STATE_INITIALIZED)
        for section, variable, array, unit in _convert_emissions(scenario):
            self._check(
                _lib.set_emissions_array(self.__state, _conv(section), _conv(variable), array.astype(np.float64), len(array)))


def _read_default_config():
    default_config = os.path.join(os.path.dirname(__file__), './rcp_default.ini')
    config = configparser.ConfigParser(inline_comment_prefixes=(';'))
    config.optionxform = str
    config.read(default_config)

    # From http://stackoverflow.com/a/3220740
    dictionary = {}
    for section in config.sections():
        dictionary[section] = {}
        for option in config.options(section):
            dictionary[section][option] = config.get(section, option)
    return dictionary


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
def _get_units():
    """Return a dict of units used in emissions file."""
    units = pd.read_csv(
        os.path.join(os.path.dirname(__file__),
            './emissions/RCP26_emissions.csv'),
        skiprows=2,
        header=None)
    return units.loc[:1, 1:].T.set_index(1).to_dict()[0]


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
    units = _get_units()
    # List of tuples [("so2", "SO2_emissions", [... array ], unit), ...]
    output = []
    for category in emissions:
        for source in emissions[category]:
            if source in scenario:
                gas = scenario[source]
                output.append((
                  category,
                  source,
                  np.array(list(zip(gas.index, gas))),
                  units[source],
                ))
    return output


def run(scenario, options=None):
    options = _read_default_config()
    with PyHector() as h:
        h.config()  # TODO options
        h.set_emissions(scenario)
        h.add_observable("temperature", "Tgav")
        h.run()
        global_temp = h.get_observable("temperature", "Tgav")
        start = int(options["core"]["startDate"])
        end = int(options["core"]["endDate"])
    return pd.Series(global_temp, index=pd.Index(range(start, end + 1)))
