#!/usr/bin/env bash
set -e

if [ -n "$PIP_PACKAGES" ]
then
    read -r -a PIP_PACKAGES <<< "$PIP_PACKAGES"
    pip install "${PIP_PACKAGES[@]}"
fi

echo
echo "#################################################"
echo
echo "Starting ${GITHUB_WORKFLOW}: ${GITHUB_ACTION}"
echo

git submodule update --init --recursive
pip install -e .

printf "%s\\n" "$@" | bash -e
