#!/usr/bin/env bash

# Assumes apt-get installed BOOST and GSL libraries
# See also https://github.com/JGCRI/hector/wiki/BuildHector

ver=`awk '/define.*BOOST_LIB_VERSION/ {print $3}' /usr/include/boost/version.hpp`
echo Boost version $ver

echo Compiling standalone Hector...
cd ../lib/hector
BOOSTLIB=/usr/local/lib   BOOSTVERSION=$ver   BOOSTROOT=/usr/include/boost \
  make hector $@

