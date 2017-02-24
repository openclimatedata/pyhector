#!/usr/bin/env bash

# Assumes apt-get installed BOOST libraries
# See also https://github.com/JGCRI/hector/wiki/BuildHector

scriptdir=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")
cd $scriptdir

echo Cloning Hector ...
git clone ../hector-wrapper/hector
cd hector
git checkout 2308fc8b53e7ab0145ba36a21334b984f111e081

ver=`awk '/define.*BOOST_LIB_VERSION/ {print $3}' /usr/include/boost/version.hpp`
echo Compiling standalone Hector in "tests/hector" directory ...
echo Boost version $ver

BOOSTLIB=/usr/local/lib   BOOSTVERSION=$ver   BOOSTROOT=/usr/include/boost \
  make hector $@
