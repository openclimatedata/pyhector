workflow "Continous Integration" {
  on = "push"
  resolves = ["Coverage"]
}

action "Black" {
  uses = "./.github/actions/run"
  args = [
    "pip install black",
    "black --check pyhector"
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
