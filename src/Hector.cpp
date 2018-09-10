/*
 * Copyright (c) 2017 Sven Willner <sven.willner@pik-potsdam.de>
 * Free software under GNU Affero General Public License v3, see LICENSE
 */

#include "Hector.h"
#include <pybind11/numpy.h>
#include <stdexcept>
#include "components/component_data.hpp"
#include "data/message_data.hpp"
#include "data/unitval.hpp"
#include "h_exception.hpp"

namespace hector = Hector;
namespace py = pybind11;

namespace pyhector {

bool Hector::Visitor::shouldVisit(bool in_spinup, double date) {
    current_date = date;
    return true;
}

void Hector::Visitor::visit(hector::Core* hcore) {
    const auto time_index = static_cast<int>(current_date - hcore->getStartDate() - 1);
    for (auto& observable : observables) {
        observable.read_data(hcore, current_date, time_index, spinup_size);
    }
    if (hcore->inSpinup()) {
        ++spinup_size;
    }
}

Hector::Hector() {
    hector::Logger& glog = hector::Logger::getGlobalLogger();
    glog.close();
    glog.open("hector", false, false, hector::Logger::LogLevel::WARNING);
    hcore.init();
    hcore.addVisitor(&visitor);
}

void Hector::add_observable(const std::string& component, std::string name, bool needs_date, bool in_spinup) {
    visitor.observables.emplace_back(Observable{&hcore, component, std::move(name), needs_date, in_spinup, run_size()});
}

py::array_t<double> Hector::get_observable(const std::string& component, const std::string& name, const bool in_spinup) const {
    for (const auto& observable : visitor.observables) {
        if (observable.matches(component, name, in_spinup)) {
            return observable.get_array();
        }
    }
    throw std::runtime_error("Observable not found");
}

int Hector::run_size() const { return static_cast<int>(hcore.getEndDate() - hcore.getStartDate()); }

int Hector::spinup_size() const { return visitor.spinup_size; }

void Hector::run() {
    visitor.spinup_size = 0;
    hcore.prepareToRun();
    hcore.run();
}

void Hector::reset() { visitor.observables.clear(); }

void Hector::set(const std::string& section, const std::string& variable, const std::string& value) {
    hector::message_data data(value);
    auto bracket_open = std::find(variable.begin(), variable.end(), '[');
    if (bracket_open != variable.end()) {
        data.date = std::stod(std::string(bracket_open + 1, std::find(bracket_open, variable.end(), ']')));
        hcore.setData(section, std::string(variable.begin(), bracket_open), data);
    } else {
        hector::message_data data(value);
        hcore.setData(section, variable, data);
    }
}

void Hector::set(const std::string& section, const std::string& variable, double value) {
    hector::message_data data(hector::unitval(value, hector::U_UNDEFINED));
    hcore.setData(section, variable, data);
}

void Hector::set(const std::string& section, const std::string& variable, int year, double value) {
    hector::message_data data(hector::unitval(value, hector::U_UNDEFINED));
    data.date = year;
    hcore.setData(section, variable, data);
}

void Hector::set(const std::string& section, const std::string& variable, const int* years, const double* values, size_t size) {
    for (unsigned int i = 0; i < size; ++i) {
        hector::message_data data(hector::unitval(values[i], hector::U_UNDEFINED));
        data.date = years[i];
        hcore.setData(section, variable, data);
    }
}

void Hector::set(const std::string& section, const std::string& variable, const std::vector<int>& years, const std::vector<double>& values) {
    if (years.size() != values.size()) {
        throw std::runtime_error("years and values should be of equal size");
    }
    set(section, variable, &years[0], &values[0], years.size());
}

void Hector::set(const std::string& section, const std::string& variable, double value, const std::string& unit) {
    hector::message_data data(hector::unitval(value, hector::unitval::parseUnitsName(unit)));
    hcore.setData(section, variable, data);
}

void Hector::set(const std::string& section, const std::string& variable, int year, double value, const std::string& unit) {
    hector::message_data data(hector::unitval(value, hector::unitval::parseUnitsName(unit)));
    data.date = year;
    hcore.setData(section, variable, data);
}

void Hector::set(const std::string& section, const std::string& variable, const int* years, const double* values, size_t size, const std::string& unit) {
    for (unsigned int i = 0; i < size; ++i) {
        hector::message_data data(hector::unitval(values[i], hector::unitval::parseUnitsName(unit)));
        data.date = years[i];
        hcore.setData(section, variable, data);
    }
}

void Hector::set(
    const std::string& section, const std::string& variable, const std::vector<int>& years, const std::vector<double>& values, const std::string& unit) {
    if (years.size() != values.size()) {
        throw std::runtime_error("years and values should be of equal size");
    }
    set(section, variable, &years[0], &values[0], years.size(), unit);
}

}  // namespace pyhector
