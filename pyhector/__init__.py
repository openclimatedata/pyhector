# -*- coding: utf-8 -*-

import ctypes
import os
import pkg_resources

import numpy as np
import pandas as pd

from .default_config import default_config
from .units import units
from .emissions import emissions

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
        for section in emissions:
            for source in emissions[section]:
                if source not in scenario.columns:
                    continue
                years = np.array(scenario.index, dtype=np.int32)
                values = np.array(scenario[source], dtype=np.float64)
                self._check(
                    _lib.set_array(
                        self.__state,
                        _conv(section),
                        _conv(source),
                        years,
                        values,
                        len(years))
                    )


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
        # In Hector 1.x RCP output value years are given as end of simulation
        # year, e.g. 1745-12-31 = 1746.0.
        # See https://github.com/JGCRI/hector/issues/177
        start = int(parameters["core"]["startDate"]) + 1
        # End of range is non-inclusive in Python ranges.
        end = int(parameters["core"]["endDate"]) + 1
        index = np.arange(start, end)
    return pd.Series(global_temp, index=index)
