#!/bin/sh

if [ -e "extern/pparse" ]; then
  echo "'extern/pparse' already exists. Remove to continue."
  exit 1
fi

if [ -z "$ORIGIN" ]; then
  echo "You must set ORIGIN envvar before running."
  exit 1
fi

mkdir -p extern
git clone $ORIGIN extern/pparse