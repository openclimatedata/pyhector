workflow "Continuous Integration" {
  on = "push"
  resolves = ["Coverage", "Documentation", "Formatting", "Linters"]
}

action "Compile" {
  uses = "./.github/actions/compile"
  args = [
    "git submodule update --init",
    "pip install -e ."
  ]
  env = {
    PYTHON_VERSION = "3.7"
  }
}

action "Documentation" {
  uses = "./.github/actions/compile"
  args = [
    "pip install -e .",
    "sphinx-build -M html docs docs/build -qW", # treat warnings as errors (-W)...
    "sphinx-build -M html docs docs/build -Eqn -b coverage", # ...but not when being nitpicky (-n)
    "if [[ -s docs/build/html/python.txt ]]",
    "then",
    "    echo",
    "    echo \"Error: Documentation missing:\"",
    "    echo",
    "    cat docs/build/html/python.txt",
    "    exit 1",
    "fi"
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "sphinx>=1.8 sphinx_rtd_theme"
  }
  needs = ["Compile"]
}

action "Formatting" {
  uses = "swillner/actions/python-run@master"
  args = [
    "black --check pyhector tests setup.py --exclude pyhector/_version.py",
    "isort --check-only --quiet --recursive pyhector tests setup.py",
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "black isort"
  }
}

action "Linters" {
  uses = "./.github/actions/compile"
  args = [
    "pip install -e .",
    "flake8 pyhector tests setup.py",
    "pylint pyhector"
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "flake8 pylint"
  }
  needs = ["Compile"]
}

action "Tests" {
  uses = "./.github/actions/compile"
  args = [
    "pip install -e .",
    "pytest tests -r a --cov=pyhector --cov-report=''",
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "pytest pytest-cov"
  }
  needs = ["Compile"]
}

action "Coverage" {
  uses = "swillner/actions/python-run@master"
  args = [
    "if ! coverage report --fail-under=\"$MIN_COVERAGE\" --show-missing",
    "then",
    "    echo",
    "    echo \"Error: Test coverage has to be at least ${MIN_COVERAGE}%\"",
    "    exit 1",
    "fi"
  ]
  env = {
    PYTHON_VERSION = "3.7"
    MIN_COVERAGE = "75"
    PIP_PACKAGES = "coverage"
  }
  needs = ["Tests"]
}


workflow "Deployment" {
  on = "create"
  resolves = ["Create release"]
}

action "Filter tag" {
  uses = "actions/bin/filter@master"
  args = "tag 'v*'"
}

action "Publish on PyPI" {
  uses = "./.github/actions/compile"
  args = [
    "git submodule update --init",
    "pip install -e .",
    "rm -rf build dist",
    "python setup.py sdist",
    "twine upload dist/*"
  ]
  env = {
    PYTHON_VERSION = "3.7"
    PIP_PACKAGES = "twine"
  }
  needs = ["Filter tag"]
  secrets = ["TWINE_USERNAME", "TWINE_PASSWORD"]
}

action "Test PyPI install" {
  uses = "./.github/actions/compile"
  args = [
    "sleep 15",
    "mkdir tmp",
    "cd tmp",
    "pip install pyhector",
    "python -c 'import pyhector'"
  ]
  env = {
    PYTHON_VERSION = "3.7"
  }
  needs = ["Publish on PyPI"]
}

action "Create release" {
  uses = "swillner/actions/create-release@master"
  needs = ["Test PyPI install"]
  secrets = ["GITHUB_TOKEN"]
}
