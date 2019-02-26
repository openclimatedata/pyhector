#!/usr/bin/env bash
set -e

if [ -n "$PIP_PACKAGES" ]
then
    pip install "$PIP_PACKAGES"
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

echo
echo "#################################################"
echo
echo "Completed ${GITHUB_WORKFLOW}: ${GITHUB_ACTION}"
