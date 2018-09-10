/*
 * Copyright (c) 2018 Sven Willner <sven.willner@pik-potsdam.de>
 * Free software under GNU Affero General Public License v3, see LICENSE
 */

#ifndef PYHECTOR_OBSERVABLE_H
#define PYHECTOR_OBSERVABLE_H

#include <pybind11/numpy.h>
#include <memory>
#include <string>
#include <vector>
#include "components/imodel_component.hpp"
#include "core/core.hpp"

namespace hector = Hector;
namespace py = pybind11;

namespace pyhector {

class Observable {
  private:
    mutable std::unique_ptr<py::array_t<double>> array;

  protected:
    hector::IModelComponent* component;
    std::string name;
    std::unique_ptr<double[]> values;
    std::size_t size;
    std::size_t reserved_size;
    bool needs_date;
    bool in_spinup;
    const std::size_t MIN_SPINUP_SIZE_RESERVED = 8;

    void resize(std::size_t new_size);

  public:
    Observable(hector::Core* hcore, const std::string& component_name, std::string name_p, bool needs_date_p, bool in_spinup_p, int expected_run_size);
    bool matches(const std::string& component_name_p, const std::string& name_p, bool in_spinup_p) const {
        return in_spinup == in_spinup_p
               && ((component == nullptr && component_name_p == CORE_COMPONENT_NAME)
                   || (component != nullptr && component_name_p == component->getComponentName()))
               && name == name_p;
    }
    void read_data(hector::Core* hcore, double current_date, int time_index, int spinup_index);
    py::array_t<double> get_array() const;
};

}  // namespace pyhector

#endif
