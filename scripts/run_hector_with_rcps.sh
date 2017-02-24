#!/usr/bin/env bash

# This script runs `hector` in the `tests/hector` directory and copies
# the output files for comparison with `pyhector`.

scriptdir=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")
cd $scriptdir
cd hector

for RF in 26 45 60 85; do
  ./source/hector input/hector_rcp$RF.ini
  cp output/outputstream_rcp$RF.csv ../tests/data
done
