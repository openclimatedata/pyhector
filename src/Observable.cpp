/*
 * Copyright (c) 2018 Sven Willner <sven.willner@pik-potsdam.de>
 * Free software under GNU Affero General Public License v3, see LICENSE
 */

#include "Observable.h"
#include <assert.h>
#include <algorithm>
#include "components/imodel_component.hpp"
#include "core/core.hpp"

namespace hector = Hector;
namespace py = pybind11;

namespace pyhector {

Observable::Observable(hector::Core* hcore, const std::string& component_name, std::string name_p, bool needs_date_p, bool in_spinup_p, int expected_run_size)
    : name(std::move(name_p)), needs_date(needs_date_p), in_spinup(in_spinup_p) {
    if (component_name == CORE_COMPONENT_NAME) {
        component = nullptr;
    } else {
        component = hcore->getComponentByName(component_name);
    }
    size = 0;
    if (in_spinup) {
        reserved_size = MIN_SPINUP_SIZE_RESERVED;
    } else {
        reserved_size = expected_run_size;
    }
    values.reset(new double[reserved_size]);
}

void Observable::read_data(hector::Core* hcore, double current_date, int time_index, int spinup_index) {
    if (in_spinup == hcore->inSpinup()) {
        hector::message_data info;
        if (needs_date) {
            info.date = current_date;
        }
        std::size_t index;
        if (in_spinup) {
            assert(spinup_index >= 0);
            index = static_cast<std::size_t>(spinup_index);
        } else {
            assert(time_index >= 0);
            index = static_cast<std::size_t>(time_index);
        }
        double value;
        if (component) {
            value = component->sendMessage(M_GETDATA, name, info);
        } else {
            value = hcore->sendMessage(M_GETDATA, name, info);
        }
        if (index >= size) {
            if (index > size) {
                std::fill_n(values.get() + index, size - index, std::numeric_limits<double>::quiet_NaN());
            }
            size = index + 1;
            if (size > reserved_size) {
                resize(2 * reserved_size);
            }
        }
        values[index] = value;
    }
}

void Observable::resize(std::size_t new_size) {
    std::unique_ptr<double[]> new_values{new double[new_size]};
    std::copy(values.get(), values.get() + size, new_values.get());
    reserved_size = new_size;
    std::swap(new_values, values);
}

py::array_t<double> Observable::get_array() const {
    if (array) {
        return *array.get();
    }
    double* data = new double[size];
    std::copy(values.get(), values.get() + size, data);

    py::capsule handle(data, [](void* d) {
        double* data = reinterpret_cast<double*>(d);
        delete[] data;
    });

    array.reset(new py::array_t<double>{{size}, data, handle});
    return *array.get();
}

}  // namespace pyhector
