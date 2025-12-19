#!/bin/sh

if [ -z "$ORIGIN" ]; then
  echo "You must set ORIGIN envvar before running."
  exit 1
fi

git clone $ORIGIN pparse