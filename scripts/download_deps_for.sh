#!/bin/sh

# !! Note: This script is intended to be run from inside a docker container.

PIP_ARGS="
  --index-url https://download.pytorch.org/whl/cpu \
  --extra-index-url https://pypi.org/simple
"

pip download $PIP_ARGS pip setuptools wheel build pytest

for arg in "$@"; do
    pip download $PIP_ARGS $arg
done
