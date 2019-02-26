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

for CMD in "$@"
do
    $CMD
done
