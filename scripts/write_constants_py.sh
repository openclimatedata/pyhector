#!/usr/bin/env bash

# Write Hector components to `../pyhector/constants.py`
# Usage:
# Run this script as
#   ./scripts/write_constants_py.sh > pyhector/constants.py

HECTOR_ROOT=./hector
HECTOR_SOURCE=$HECTOR_ROOT/src
HECTOR_HEADERS=$HECTOR_ROOT/inst/include

echo '"""'
echo 'Internal mapping of Hector components and variables.'
echo 'Auto-generated from Hector headers.'
echo -e '"""\n'

echo 'components = {'; \
(echo '#include "hector/inst/include/component_names.hpp"'; \
  sed -n -e 's/^#define *\([^[:space:]]*\).*$/v\1=\1;/p' \
      $HECTOR_HEADERS/component_names.hpp) \
		| gcc -E -I $HECTOR_HEADERS - \
		| sed -n -e 's/" "//g;s/^v\(.*\)_COMPONENT_NAME="\(.*\)";$/    "\1": "\2",/p'; \
		echo '}'; #\
		echo -e '\nvariables = {'; \
		(echo '#include "hector/inst/include/component_data.hpp"'; \
			sed -n -e 's/^#define  *\([^[:space:]]*\).*$/v\1=\1;/p' $HECTOR_HEADERS/component_data.hpp) \
		| gcc -E -I $HECTOR_HEADERS - \
		| sed -n -e 's/" "//g;s/^vD_\(.*\)="\(.*\)";$/    "\1": "\2",/p'; \
		echo '}'
