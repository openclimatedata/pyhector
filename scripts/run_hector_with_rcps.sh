#!/usr/bin/env bash

cd ../lib/hector

for RF in 26 45 60 85; do
  ./source/hector input/hector_rcp$RF.ini
  cp output/outputstream_rcp$RF.csv ../../tests/data
done
