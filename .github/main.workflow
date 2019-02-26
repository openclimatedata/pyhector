workflow "Continous Integration" {
  on = "push"
  resolves = ["Bandit", "Black", "Coverage", "Pylint"]
}

action "Bandit" {
  uses = "./.github/actions/run"
  args = [
    "pip install bandit",
    "bandit -c .bandit.yml -r ."
  ]
  env = {
    PYTHON_VERSION = "3.7"
  }
}

action "Black" {
  uses = "./.github/actions/run"
  args = [
    "pip install black",
    "black --check pyhector tests"
  ]
  env = {
    PYTHON_VERSION = "3.7"
  }
}

action "Coverage" {
  uses = "./.github/actions/coverage"
  env = {
    PYTHON_VERSION = "3.7"
    MIN_COVERAGE = "75"
  }
  secrets = ["CODECOV_TOKEN"]
}

action "Pylint" {
  uses = "./.github/actions/run"
  args = [
    "pip install pylint",
    "pylint pyhector"
  ]
  env = {
    PYTHON_VERSION = "3.7"
  }
}
