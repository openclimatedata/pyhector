#include <exception>
#include <vector>
#include <string>
#include <string.h>
#include "HectorWrapper.h"
#include "core/core.hpp"
#include "core/logger.hpp"
#include "data/message_data.hpp"
#include "components/component_data.hpp"
#include "data/unitval.hpp"
#include "h_exception.hpp"
#include "visitors/avisitor.hpp"
#include "components/imodel_component.hpp"

extern "C" {

static std::string last_error;

const char* hector_get_last_error() { return last_error.c_str(); }

int hector_open(Hector::HectorWrapper** wrapper) {
    try {
        *wrapper = new Hector::HectorWrapper();
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int hector_set_value(Hector::HectorWrapper* wrapper, const char* section, const char* variable, const char* value) {
    try {
        wrapper->set(section, variable, value);
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int hector_set_array(Hector::HectorWrapper* wrapper, const char* component, const char* name, const int* years, const double* values, const size_t size) {
    try {
        wrapper->set(component, name, years, values, size);
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int hector_add_observable(Hector::HectorWrapper* wrapper, const char* component, const char* name, const bool needs_date) {
    try {
        wrapper->output()->add_variable(component, name, needs_date);
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int hector_get_observable(Hector::HectorWrapper* wrapper, const char* component, const char* name, double* output) {
    try {
        const std::vector<double>& result = wrapper->output()->get_variable(component, name);
        memcpy(output, &result[0], wrapper->output()->run_size() * sizeof(double));
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int hector_run(Hector::HectorWrapper* wrapper) {
    try {
        wrapper->hcore()->prepareToRun();
        wrapper->hcore()->run();
        return wrapper->output()->run_size();
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int hector_close(Hector::HectorWrapper* wrapper) {
    try {
        delete wrapper;
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}
}
