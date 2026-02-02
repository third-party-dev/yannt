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

pip download $PIP_ARGS $PY_CONSTRAINTS_ARGS $PIP_PKGS

#  pip setuptools wheel build pytest ipykernel cmake \
#  Cython meson-python ninja patchelf

# Do given python packages
for arg in "$@"; do
    pip download $PIP_ARGS $PY_CONSTRAINTS_ARGS $arg
done

# Do extern python packages
for ext in `ls -1 /work/extern`; do
    pip download $PIP_ARGS $PY_CONSTRAINTS_ARGS /work/extern/$ext
done
