#!/usr/bin/env bash

# This script runs `hector` and copies
# the output files for comparison with `pyhector`.

scriptdir=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")
cd $scriptdir/../hector/inst

for RF in 26 45 60 85; do
  ../src/hector input/hector_rcp$RF.ini
  cp output/outputstream_rcp$RF.csv $scriptdir/../tests/data
done
