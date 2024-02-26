#!/usr/bin/env bash

# This script runs `hector` and copies
# the output files for comparison with `pyhector`.

scriptdir=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")
cd $scriptdir/../hector/inst

for SSP in 119 126 245 370 434 460 534-over 585; do
  ../src/hector input/hector_ssp$SSP.ini
  cp output/outputstream_ssp$SSP.csv $scriptdir/../tests/data
done
