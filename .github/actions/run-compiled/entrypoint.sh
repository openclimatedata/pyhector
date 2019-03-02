#!/usr/bin/env bash
set -e

if [ -n "$PIP_PACKAGES" ]
then
    read -r -a PIP_PACKAGES <<< "$PIP_PACKAGES"
    pip install "${PIP_PACKAGES[@]}"
fi

git submodule init
while ! git submodule update # Filesystem quirks with Github actions?
do
    sleep 2
done

mkdir /tmp/build
ln -s /tmp/build ./build
pip install -e .

echo
echo "################################################################################"
echo

printf "%s\\n" "$@" | bash -e
