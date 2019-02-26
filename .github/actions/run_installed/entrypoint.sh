#!/usr/bin/env bash
set -e

if [ -n "$PIP_PACKAGES" ]
then
    read -r -a PIP_PACKAGES <<< "$PIP_PACKAGES"
    pip install "${PIP_PACKAGES[@]}"
fi

git submodule update --init \
    || (sleep 1; git submodule update --init) # Prevent occasional hiccup
pip install -e .

echo
echo "################################################################################"
echo

printf "%s\\n" "$@" | bash -e
