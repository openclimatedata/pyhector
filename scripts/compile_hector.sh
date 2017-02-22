#!/usr/bin/env bash

# Assumes apt-get installed BOOST libraries
# See also https://github.com/JGCRI/hector/wiki/BuildHector

ver=`awk '/define.*BOOST_LIB_VERSION/ {print $3}' /usr/include/boost/version.hpp`
echo Compiling standalone Hector in "tests/hector" directory ...
echo Boost version $ver

scriptdir=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")

cd $scriptdir
cd ../tests/hector
BOOSTLIB=/usr/local/lib   BOOSTVERSION=$ver   BOOSTROOT=/usr/include/boost \
  make hector $@

