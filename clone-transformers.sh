#!/bin/sh

if [ -e "extern/thirdparty_yannt_transformers" ]; then
  echo "'extern/thirdparty_yannt_transformers' already exists. Remove to continue."
  exit 1
fi

if [ -z "$ORIGIN" ]; then
  echo "You must set ORIGIN envvar before running."
  exit 1
fi

mkdir -p extern
git clone $ORIGIN extern/thirdparty_yannt_transformers