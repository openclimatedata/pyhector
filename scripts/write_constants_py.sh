#!/usr/bin/env bash

# Write Hector components to `../pyhector/constants.py`
# Usage:
# Run this script as
#   ./write_constants_py.sh > ../pyhector/constants.py

HECTOR_ROOT=../src/hector
HECTOR_SOURCE=$HECTOR_ROOT/source
HECTOR_HEADERS=$HECTOR_ROOT/headers

echo 'components = {'; \
(echo '#include "components/component_names.hpp"'; \
  sed -n -e 's/^#define *\([^[:space:]]*\).*$/v\1=\1;/p' \
      $HECTOR_HEADERS/components/component_names.hpp) \
		| gcc -E -I $HECTOR_HEADERS - \
		| sed -n -e 's/" "//g;s/^v\(.*\)_COMPONENT_NAME="\(.*\)";$/    "\1": "\2",/p'; \
		echo '}'; #\
		echo 'variables = {'; \
		(echo '#include "components/component_data.hpp"'; \
			sed -n -e 's/^#define  *\([^[:space:]]*\).*$/v\1=\1;/p' $HECTOR_HEADERS/components/component_data.hpp) \
		| gcc -E -I $HECTOR_HEADERS - \
		| sed -n -e 's/" "//g;s/^vD_\(.*\)="\(.*\)";$/    "\1": "\2",/p'; \
		echo '}'
