#include <vector>
#include <string>
#include <string.h>
#include "core/core.hpp"
#include "core/logger.hpp"
#include "data/message_data.hpp"
#include "components/component_data.hpp"
#include "data/unitval.hpp"
#include "h_exception.hpp"
#include "visitors/avisitor.hpp"
#include "components/imodel_component.hpp"

class State;

class OutputVisitor : public Hector::AVisitor {

  private:
    double start_date;
    double end_date;
    int index;
    struct OutputVariable {
        Hector::IModelComponent* component;
        std::string name;
        std::vector<double> values;
    };
    std::vector<OutputVariable> variables;

  public:
    void add_variable(const State* state, const std::string& component, const std::string& name);
    double* get_variable(const State* state, const std::string& component, const std::string& name);
    bool shouldVisit(const bool in_spinup, const double date);
    void visit(Hector::Core* core);
    int run_size(const State* state);
};

class State {
  private:
    Hector::Core hcore_;
    OutputVisitor output_visitor;

  public:
    State() {
        Hector::Logger& glog = Hector::Logger::getGlobalLogger();
        glog.close();
        glog.open("hector", false, Hector::Logger::WARNING, false);
        hcore_.init();
        hcore_.addVisitor(&output_visitor);
    }

    ~State() {}

    inline OutputVisitor* output() { return &output_visitor; }

    inline Hector::Core* hcore() { return &hcore_; }
    inline const Hector::Core* hcore() const { return &hcore_; }
};

void OutputVisitor::add_variable(const State* state, const std::string& component, const std::string& name) {
    start_date = state->hcore()->getStartDate();
    Hector::IModelComponent* component_;
    if (component == "core") {
        component_ = 0;
    } else {
        component_ = state->hcore()->getComponentByName(component);
    }
    OutputVariable variable = {
        component_,
        name,
        std::vector<double>(static_cast<int>(state->hcore()->getEndDate() - start_date))
    };
    variables.push_back(variable);
}

double* OutputVisitor::get_variable(const State* state, const std::string& component, const std::string& name) {
    for (std::vector<OutputVariable>::iterator variable = variables.begin(); variable != variables.end(); ++variable) {
        if (name == variable->name && component == variable->component->getComponentName()) {
            return &variable->values[0];
        }
    }
    return 0;
}

bool OutputVisitor::shouldVisit(const bool in_spinup, const double date) {
    index = static_cast<int>(date - start_date - 1); // date is at the end of the timestep
    return !in_spinup;
}

void OutputVisitor::visit(Hector::Core* core) {
    for (std::vector<OutputVariable>::iterator variable = variables.begin(); variable != variables.end(); ++variable) {
        if (variable->component) {
            variable->values[index] = variable->component->sendMessage(M_GETDATA, variable->name);
        } else {
            variable->values[index] = core->sendMessage(M_GETDATA, variable->name);
        }
    }
};

int OutputVisitor::run_size(const State* state) {
    return static_cast<int>(state->hcore()->getEndDate() - start_date);
}

static std::string last_error;

extern "C" {

const char* get_last_error() { return last_error.c_str(); }

int open(State** state) {
    try {
        *state = new State();
        return 0;
    } catch (const h_exception& he) {
        last_error = he.msg;
        return -1;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -2;
    }
}

int set_config_value(State* state, const char* section, const char* variable, const char* value) {
    try {
        Hector::message_data data(value);
        state->hcore()->setData(section, variable, data);
        return 0;
    } catch (const h_exception& he) {
        last_error = he.msg;
        return -1;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -2;
    }
}

int set_config_timed_value(State* state, const char* section, const char* variable, const double year, const char* value) {
    try {
        Hector::message_data data(value);
        data.date = year;
        state->hcore()->setData(section, variable, data);
        return 0;
    } catch (const h_exception& he) {
        last_error = he.msg;
        return -1;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -2;
    }
}

int set_emissions(State* state, const char* component, const char* name, const double year, const double value) {
    try {
        Hector::message_data data(value);
        data.date = year;
        state->hcore()->setData(component, name, data);
        return 0;
    } catch (const h_exception& he) {
        last_error = he.msg;
        return -1;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -2;
    }
}

int set_emissions_array(State* state, const char* component, const char* name, const double* values, const size_t size) {
    try {
        for (unsigned int i = 0; i < size; ++i) {
            Hector::message_data data(Hector::unitval(values[2 * i + 1], Hector::U_UNDEFINED));
            data.date = values[2 * i];
            state->hcore()->setData(component, name, data);
        }
        return 0;
    } catch (const h_exception& he) {
        last_error = he.msg;
        return -1;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -2;
    }
}

int add_observable(State* state, const char* component, const char* name) {
    try {
        state->output()->add_variable(state, component, name);
        return 0;
    } catch (const h_exception& he) {
        last_error = he.msg;
        return -1;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -2;
    }
}

int get_observable(State* state, const char* component, const char* name, double* output) {
    try {
        double* result = state->output()->get_variable(state, component, name);
        if (!result) {
            last_error = "Variable not found";
            return -2;
        }
        memcpy(output, result, state->output()->run_size(state) * sizeof(double));
        return 0;
    } catch (const h_exception& he) {
        last_error = he.msg;
        return -1;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -2;
    }
}

int run(State* state) {
    try {
        state->hcore()->prepareToRun();
        state->hcore()->run();
        return state->output()->run_size(state);
    } catch (const h_exception& he) {
        last_error = he.msg;
        return -1;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -2;
    }
}

int close(State* state) {
    try {
        delete state;
        return 0;
    } catch (const std::exception& ex) {
        last_error = ex.what();
        return -2;
    }
}
}
