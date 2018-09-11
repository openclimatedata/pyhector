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

namespace Hector {
class IModelComponent;
class Core;
}  // namespace Hector

namespace hector = Hector;
namespace py = pybind11;

namespace pyhector {

class Observable {
  private:
    mutable std::unique_ptr<py::array_t<double>> array;

  protected:
    std::string component_name;
    std::string name;
    bool needs_date;
    bool in_spinup;
    std::size_t expected_run_size;
    hector::IModelComponent* component;
    std::vector<double> values;

  public:
    Observable(hector::Core* hcore, std::string component_name_p, std::string name_p, bool needs_date_p, bool in_spinup_p, std::size_t expected_run_size_p);
    bool matches(const std::string& component_name_p, const std::string& name_p, bool in_spinup_p) const;
    void read_data(hector::Core* hcore, double current_date, std::size_t time_index, std::size_t spinup_index);
    void reset(hector::Core* hcore);
    py::array_t<double> get_array() const;
};

}  // namespace pyhector

#endif
