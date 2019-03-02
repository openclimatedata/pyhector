#!/usr/bin/env bash
set -e

if [ -n "$PIP_PACKAGES" ]
then
    read -r -a PIP_PACKAGES <<< "$PIP_PACKAGES"
    pip install "${PIP_PACKAGES[@]}"
fi

while ! git submodule update # Filesystem quirks with Github actions?
do
    sleep 2
done

mkdir /tmp/build
python setup.py \
       build_ext \
       --parallel 1 \
       --build-lib /tmp/build

sleep 1
echo
echo "Installing"
echo
pip install .

echo
echo "################################################################################"
echo

printf "%s\\n" "$@" | bash -e
