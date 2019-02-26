#!/usr/bin/env bash
set -e

echo
echo "#################################################"
echo
echo "Starting ${GITHUB_WORKFLOW}: ${GITHUB_ACTION}"
echo

git submodule update --init
pip install -e .
pytest --cov
if ! coverage report --fail-under="$MIN_COVERAGE"
then
    echo
    echo "Error: Coverage has to be at least ${MIN_COVERAGE}%"
    exit 1
fi

echo
echo "#################################################"
echo
echo "Completed ${GITHUB_WORKFLOW}: ${GITHUB_ACTION}"
