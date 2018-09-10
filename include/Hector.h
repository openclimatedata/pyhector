/*
 * Copyright (c) 2017, 2018 Sven Willner <sven.willner@pik-potsdam.de>
 * Free software under GNU Affero General Public License v3, see LICENSE
 */

#ifndef PYHECTOR_HECTOR_H
#define PYHECTOR_HECTOR_H

#include <pybind11/numpy.h>
#include <string>
#include <vector>
#include "Observable.h"
#include "core/core.hpp"
#include "visitors/avisitor.hpp"

namespace hector = Hector;
namespace py = pybind11;

namespace pyhector {

class Hector {
  protected:
    class Visitor : hector::AVisitor {
        friend class Hector;

      protected:
        double current_date;
        std::vector<Observable> observables;
        int spinup_size;

      public:
        bool shouldVisit(const bool in_spinup, const double date);
        void visit(hector::Core* core);
    };

    Visitor visitor;
    hector::Core hcore;

  public:
    Hector();
    void add_observable(const std::string& component, std::string name, bool need_date, bool in_spinup);
    py::array_t<double> get_observable(const std::string& component, const std::string& name, bool in_spinup) const;
    int run_size() const;
    int spinup_size() const;
    void reset();
    void run();
    void set(const std::string& section, const std::string& variable, const std::string& value);
    void set(const std::string& section, const std::string& variable, double value);
    void set(const std::string& section, const std::string& variable, int year, double value);
    void set(const std::string& section, const std::string& variable, const int* years, const double* values, size_t size);
    void set(const std::string& section, const std::string& variable, const std::vector<int>& years, const std::vector<double>& values);
    void set(const std::string& section, const std::string& variable, double value, const std::string& unit);
    void set(const std::string& section, const std::string& variable, int year, double value, const std::string& unit);
    void set(const std::string& section, const std::string& variable, const int* years, const double* values, size_t size, const std::string& unit);
    void set(
        const std::string& section, const std::string& variable, const std::vector<int>& years, const std::vector<double>& values, const std::string& unit);
};

}  // namespace pyhector

#endif
