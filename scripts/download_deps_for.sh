#!/bin/sh

# !! Note: This script is intended to be run from inside a docker container.

PROJ_PATH=$(realpath $(dirname $0)/..)
cd $PROJ_PATH

PY_CONSTRAINTS=${PY_CONSTRAINTS:-}
if [ -n "${PY_CONSTRAINTS}" ]; then
    PY_CONSTRAINTS_ARGS="-c ${PY_CONSTRAINTS}"
else
    PY_CONSTRAINTS_ARGS=
fi

echo PIP_ARGS: ${PIP_ARGS}

pip download $PIP_ARGS $PY_CONSTRAINTS_ARGS pip setuptools wheel build pytest ipykernel cmake

for arg in "$@"; do
    pip download $PIP_ARGS $PY_CONSTRAINTS_ARGS $arg
done
