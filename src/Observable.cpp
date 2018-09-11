/*
 * Copyright (c) 2018 Sven Willner <sven.willner@pik-potsdam.de>
 * Free software under GNU Affero General Public License v3, see LICENSE
 */

#include "Observable.h"
#include <algorithm>
#include <limits>
#include "components/imodel_component.hpp"
#include "core/core.hpp"

namespace hector = Hector;
namespace py = pybind11;

namespace pyhector {

Observable::Observable(
    hector::Core* hcore, std::string component_name_p, std::string name_p, bool needs_date_p, bool in_spinup_p, std::size_t expected_run_size_p)
    : component_name(std::move(component_name_p)),
      name(std::move(name_p)),
      needs_date(needs_date_p),
      in_spinup(in_spinup_p),
      expected_run_size(expected_run_size_p) {
    reset(hcore);
}

void Observable::read_data(hector::Core* hcore, double current_date, std::size_t time_index, std::size_t spinup_index) {
    if (in_spinup == hcore->inSpinup()) {
        hector::message_data info;
        if (needs_date) {
            info.date = current_date;
        }

        std::size_t index;
        if (in_spinup) {
            index = spinup_index;
        } else {
            index = time_index;
        }

        double value;
        if (component) {
            value = component->sendMessage(M_GETDATA, name, info);
        } else {
            value = hcore->sendMessage(M_GETDATA, name, info);
        }

        if (index >= values.size()) {
            values.resize(index + 1, std::numeric_limits<double>::quiet_NaN());
        }
        values[index] = value;
        array.reset();
    }
}

void Observable::reset(hector::Core* hcore) {
    if (component_name == CORE_COMPONENT_NAME) {
        component = nullptr;
    } else {
        component = hcore->getComponentByName(component_name);
    }
    values.clear();
    if (!in_spinup) {
        values.reserve(expected_run_size);
    }
    array.reset();
}

bool Observable::matches(const std::string& component_name_p, const std::string& name_p, bool in_spinup_p) const {
    return in_spinup == in_spinup_p
           && ((component == nullptr && component_name_p == CORE_COMPONENT_NAME) || (component != nullptr && component_name_p == component->getComponentName()))
           && name == name_p;
}

py::array_t<double> Observable::get_array() const {
    if (array) {
        return *array.get();
    }
    double* data = new double[values.size()];
    std::copy(std::begin(values), std::end(values), data);

    py::capsule handle(data, [](void* d) {
        double* data = reinterpret_cast<double*>(d);
        delete[] data;
    });

    array.reset(new py::array_t<double>{{values.size()}, data, handle});
    return *array.get();
}

}  // namespace pyhector
