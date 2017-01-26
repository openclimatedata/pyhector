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

const char* get_last_error() { return last_error.c_str(); }

int open(Hector::HectorWrapper** wrapper) {
    try {
        *wrapper = new Hector::HectorWrapper();
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int set_value(Hector::HectorWrapper* wrapper, const char* section, const char* variable, const char* value) {
    try {
        wrapper->set(section, variable, value);
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int set_array(Hector::HectorWrapper* wrapper, const char* component, const char* name, const int* years, const double* values, const size_t size) {
    try {
        wrapper->set(component, name, years, values, size);
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int add_observable(Hector::HectorWrapper* wrapper, const char* component, const char* name) {
    try {
        wrapper->output()->add_variable(component, name);
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int get_observable(Hector::HectorWrapper* wrapper, const char* component, const char* name, double* output) {
    try {
        const std::vector<double>& result = wrapper->output()->get_variable(component, name);
        memcpy(output, &result[0], wrapper->output()->run_size() * sizeof(double));
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int run(Hector::HectorWrapper* wrapper) {
    try {
        wrapper->hcore()->prepareToRun();
        wrapper->hcore()->run();
        return wrapper->output()->run_size();
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}

int close(Hector::HectorWrapper* wrapper) {
    try {
        delete wrapper;
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -1;
    }
}
}
