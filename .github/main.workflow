workflow "Continuous Integration" {
  on = "push"
  resolves = ["Bandit", "Black", "Pylint", "Test coverage"]
}

action "Bandit" {
  uses = "swillner/actions/python-run@master"
  args = [
    "bandit -c .bandit.yml -r ."
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "bandit"
  }
}

action "Black" {
  uses = "swillner/actions/python-run@master"
  args = [
    "black --check pyhector tests setup.py --exclude pyhector/_version.py"
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "black"
  }
}

action "Pylint" {
  uses = "./.github/actions/run_installed"
  args = [
    "pylint pyhector"
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "pylint"
  }
}

action "Test coverage" {
  uses = "./.github/actions/run_installed"
  args = [
    "pytest --cov",
    "if ! coverage report --fail-under=\"$MIN_COVERAGE\"",
    "then",
    "    echo",
    "    echo \"Error: Coverage has to be at least ${MIN_COVERAGE}%\"",
    "    exit 1",
    "fi"
  ]
  env = {
    PYTHON_VERSION = "3.7"
    MIN_COVERAGE = "75"
    PIP_PACKAGES = "coverage pytest pytest-cov"
  }
}


workflow "Deployment" {
  on = "release"
  resolves = ["Create release"]
}

action "Filter tag" {
  uses = "actions/bin/filter@master"
  args = "tag v*"
}

action "Publish on PyPi" {
  uses = "./.github/actions/run_installed"
  args = [
    "rm -rf build dist",
    "python setup.py sdist",
    "twine upload dist/*"
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "twine"
  }
  needs = ["Filter tag", "Bandit", "Black", "Pylint", "Test coverage"]
  secrets = ["TWINE_USERNAME", "TWINE_PASSWORD"]
}

action "Create release" {
  uses = "swillner/actions/create-release@master"
  needs = ["Publish on PyPi"]
  secrets = ["GITHUB_TOKEN"]
}
