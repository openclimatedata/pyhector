/*
 * Copyright (c) 2018 Sven Willner <sven.willner@pik-potsdam.de>
 * Free software under GNU Affero General Public License v3, see LICENSE
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Hector.h"
#include "Observable.h"
#include "h_exception.hpp"

namespace py = pybind11;

namespace pyhector {

PYBIND11_MODULE(model, m) {
    m.doc() = R"pbdoc(
        pyhector.model
        --------------

        `pyhector` is a Python wrapper for the simple global climate
        carbon-cycle model Hector (https://github.com/JGCRI/hector).

        See README.rst and repository for details:
        https://github.com/openclimatedata/pyhector
    )pbdoc";

    static py::exception<h_exception> hector_exception(m, "HectorException");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) {
                std::rethrow_exception(p);
            }
        } catch (const h_exception& e) {
            hector_exception(e.what());
        }
    });

    py::class_<Hector>(m, "Hector", "Class providing an interface to Hector")
        .def(py::init())
        .def_property_readonly("run_size", &Hector::spinup_size, "Number of steps to run")
        .def_property_readonly("spinup_size", &Hector::spinup_size, "Number of spinup steps run")
        .def("add_observable", &Hector::add_observable,
             R"doc(
                   Set a variable that can be read later.
                   See :mod:`pyhector.output` for available components and variables.

                   Parameters
                   ----------
                   component : str
                       Name of Hector component
                   name : string
                       Name of variable in component
                   needs_date : bool, default ``False``
                       Whether variable needs a date
                   in_spinup : bool, default ``False``
                       True to return from spinup phase, else from run phase
            )doc",
             py::arg("component"), py::arg("name"), py::arg("needs_date") = false, py::arg("in_spinup") = false)
        .def("get_observable", &Hector::get_observable,
             R"doc(
                   Returns output variable.
                   See :mod:`pyhector.output` for available variables.

                   Parameters
                   ----------
                   component : str
                       Name of Hector component
                   name : string
                       Name of variable in component
                   in_spinup : bool, default ``False``
                       True to return from spinup phase, else from run phase. Must have
                       been set in :py:meth:`add_observable` accordingly
             )doc",
             py::arg("component"), py::arg("name"), py::arg("in_spinup") = false)
        .def("_set", (void (Hector::*)(const std::string&, const std::string&, const std::string&)) & Hector::set, "Set Parameters.")
        .def("_set", (void (Hector::*)(const std::string&, const std::string&, double)) & Hector::set, "Set Parameters.")
        .def("_set", (void (Hector::*)(const std::string&, const std::string&, double, const std::string&)) & Hector::set, "Set Parameters.")
        .def("_set", (void (Hector::*)(const std::string&, const std::string&, int, double)) & Hector::set, "Set Parameters.")
        .def("_set", (void (Hector::*)(const std::string&, const std::string&, int, double, const std::string&)) & Hector::set, "Set Parameters.")
        .def("_set", (void (Hector::*)(const std::string&, const std::string&, const std::vector<int>&, const std::vector<double>&)) & Hector::set,
             "Set Parameters.")
        .def("_set",
             (void (Hector::*)(const std::string&, const std::string&, const std::vector<int>&, const std::vector<double>&, const std::string&)) & Hector::set,
             "Set Parameters.")
        .def("run", &Hector::run, "Run Hector.");
}

}  // namespace pyhector
