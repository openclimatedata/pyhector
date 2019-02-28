#!/usr/bin/env bash

# Assumes apt-get installed BOOST libraries
# See also https://github.com/JGCRI/hector/wiki/BuildHector

scriptdir=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")
cd $scriptdir/../hector


ver=`awk '/define.*BOOST_LIB_VERSION/ {print $3}' /usr/include/boost/version.hpp`
echo Compiling standalone Hector ...
echo Boost version $ver

BOOSTLIB=/usr/local/lib   BOOSTVERSION=$ver   BOOSTROOT=/usr/include/boost \
  make hector $@
