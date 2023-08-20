#!/bin/bash

if [ ! -f "radloggerpy/locale/radloggerpy.pot.ref" ]; then
  echo "File radloggerpy/locale/radloggerpy.pot.ref does not exist!"
  exit 1
fi

diff -I '^#' -I '^ #' <(tail -n +19 radloggerpy/locale/radloggerpy.pot) <(tail -n +19 radloggerpy/locale/radloggerpy.pot.ref)