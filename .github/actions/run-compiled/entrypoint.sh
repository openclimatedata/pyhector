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
sleep 1
git submodule update
sleep 1

pip install . \
    --install-option "-j 1" \
    --install-option "--build-temp"

echo
echo "################################################################################"
echo

printf "%s\\n" "$@" | bash -e
