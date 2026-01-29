#!/bin/sh

# !! Note: This script is intended to be run from inside a docker container.

pip download $PIP_ARGS pip setuptools wheel build pytest ipykernel

for arg in "$@"; do
    pip download $PIP_ARGS $arg
done
