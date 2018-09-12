/*
 * Copyright (c) 2018 Sven Willner <sven.willner@pik-potsdam.de>
 * Free software under GNU Affero General Public License v3, see LICENSE
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Hector.h"
#include "Observable.h"
#include "h_exception.hpp"
#include "h_util.hpp"

namespace py = pybind11;

namespace pyhector {

PYBIND11_MODULE(_binding, m) {
    m.doc() = R"pbdoc(
        pyhector._binding
        -----------------

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

    py::class_<Hector>(m, "_Hector", "Class providing an interface to Hector")
        .def(py::init())
        .def_property_readonly("run_size", &Hector::run_size, "Number of steps to run by default")
        .def_property_readonly("spinup_size", &Hector::spinup_size, "Number of spinup steps run")
        .def_property_readonly("start_date", &Hector::start_date, "Start date")
        .def_property_readonly("end_date", &Hector::end_date, "End date")
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
        .def("clear_observables", &Hector::clear_observables, "Clear observables registered so far.")
        .def("reset", &Hector::reset, "(Hard) reset Hector.")
        .def("run", &Hector::run,
             R"doc(
                   Run Hector.

                   Parameters
                   ----------
                   until : double, default ``None``
                       Year to run until (including) or run till end date as given by
                       configuration if None
             )doc",
             py::arg("until") = py::none())
        .def("shutdown", &Hector::shutdown, "Shutdown Hector.")
        .def("_set_string", (void (Hector::*)(const std::string&, const std::string&, const std::string&)) & Hector::set, "Set Parameters.")
        .def("_set_double", (void (Hector::*)(const std::string&, const std::string&, double)) & Hector::set, "Set Parameters.")
        .def("_set_double_unit", (void (Hector::*)(const std::string&, const std::string&, double, const std::string&)) & Hector::set, "Set Parameters.")
        .def("_set_timed_double", (void (Hector::*)(const std::string&, const std::string&, std::size_t, double)) & Hector::set, "Set Parameters.")
        .def("_set_timed_double_unit", (void (Hector::*)(const std::string&, const std::string&, std::size_t, double, const std::string&)) & Hector::set,
             "Set Parameters.")
        .def("_set_timed_array",
             (void (Hector::*)(const std::string&, const std::string&, const std::vector<std::size_t>&, const std::vector<double>&)) & Hector::set,
             "Set Parameters.")
        .def("_set_timed_array_unit",
             (void (Hector::*)(const std::string&, const std::string&, const std::vector<std::size_t>&, const std::vector<double>&, const std::string&))
                 & Hector::set,
             "Set Parameters.");

    m.attr("__hector_version__") = MODEL_VERSION;
}

}  // namespace pyhector
