#!/usr/bin/env bash
set -e

if [ -n "$PIP_PACKAGES" ]
then
    read -r -a PIP_PACKAGES <<< "$PIP_PACKAGES"
    pip install "${PIP_PACKAGES[@]}"
fi

sleep 1  # Filesystem quirks with Github actions?
git submodule init
sleep 1
git submodule sync
sleep 2
git submodule update
sleep 1

python setup.py build-ext --parallel 1 --build-temp

sleep 1
echo
echo "Installing"
echo
pip install .

echo
echo "################################################################################"
echo

printf "%s\\n" "$@" | bash -e
