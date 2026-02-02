#!/usr/bin/env bash

# TODO: Check if PY_VER is set.

PROJ_PATH=$(realpath $(dirname $0)/..)

export PY_VER=${PY_VER:-$(python3 --version | awk '{print $2}' | cut -d. -f1,2)}

# Allow user to assign venv name and tag shell prompt
export ML_VENV_NAME=${ML_VENV_NAME:-ml-venv-${PY_VER}-dud}
export PS1_TAG="(${ML_VENV_NAME}) "
export PS1="${PS1_TAG}${PS1:-\$ }"

# Default to using system python version. Expecting only major.minor (e.g 3.13)
PIP_ARGS="
  --index-url https://download.pytorch.org/whl/cpu \
  --extra-index-url https://pypi.org/simple
"

# Do the local install
docker run -ti --rm \
  -u $(id -u):$(id -g) \
  -v ${PROJ_PATH}:/work -w /work \
  -e PIP_ARGS="${PIP_ARGS}" \
  -e HOME=/work \
  -e ML_VENV_NAME="${ML_VENV_NAME}" \
  -e PY_VER="${PY_VER}" \
  -e PS1_TAG="${PS1_TAG}" \
  -e PS1="${PS1}" \
  python:${PY_VER}-slim \
  /work/scripts/build-dev-venv.sh
