#!/bin/sh

# !! Note: This script is intended to be run from inside a docker container.

# Vars needed to be passed:
# - PY_CONSTRAINTS
# - PY_REQS
# - PIP_IDX_ARGS
# - PY_VER
# - 

# Note: PROJ_PATH here should eval to the same as DOCKER_PROJ_PATH
#PROJ_PATH=$(realpath $(dirname $0)/..)
cd ${CRI_PROJ_PATH}

PY_CONSTRAINTS=${PY_CONSTRAINTS:-}
if [ -n "${PY_CONSTRAINTS}" ]; then
    PY_CONSTRAINTS_ARGS="-c ${PY_CONSTRAINTS}"
else
    PY_CONSTRAINTS_ARGS=
fi

PY_REQS=${PY_REQS:-}
if [ -n "${PY_REQS}" ]; then
    PY_REQS_ARGS="-r ${PY_REQS}"
else
    PY_REQS_ARGS=
fi

PIP_DL_ARGS=${PIP_DL_ARGS:-"${PIP_IDX_ARGS} -d ./cache/pip_pkgs/${PY_VER}"}
mkdir -p ./cache/pip_pkgs/${PY_VER}

echo PIP_DL_ARGS: ${PIP_DL_ARGS}

pip download ${PIP_DL_ARGS} ${PY_REQS_ARGS} ${PY_CONSTRAINTS_ARGS}

# # Do given python packages
# for arg in "$@"; do
#     pip download $PIP_ARGS $PY_CONSTRAINTS_ARGS $arg
# done
# Do it for yannt
pip download ${PIP_DL_ARGS} ${PY_CONSTRAINTS_ARGS} ./yannt

# Do extern python packages
for ext in `ls -1 ./extern`; do
    pip download ${PIP_DL_ARGS} ${PY_CONSTRAINTS_ARGS} ./extern/$ext
done

