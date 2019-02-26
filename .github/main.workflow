workflow "Continous Integration" {
  on = "push"
  resolves = ["Bandit", "Black", "Coverage", "Pylint"]
}

action "Bandit" {
  uses = "./.github/actions/run"
  args = [
    "bandit -c .bandit.yml -r ."
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "bandit"
  }
}

action "Black" {
  uses = "./.github/actions/run"
  args = [
    "black --check pyhector tests"
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "black"
  }
}

action "Coverage" {
  uses = "./.github/actions/coverage"
  env = {
    PYTHON_VERSION = "3.7"
    MIN_COVERAGE = "75"
  }
}

action "Pylint" {
  uses = "./.github/actions/run"
  args = [
    "pylint pyhector"
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "pylint"
  }
}
