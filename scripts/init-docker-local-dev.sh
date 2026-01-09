#!/usr/bin/env bash

# TODO: Check if PY_VER is set.

PROJ_PATH=$(realpath $(dirname $0)/..)

export PY_VER=${PY_VER:-$(python3 --version | awk '{print $2}' | cut -d. -f1,2)}

${PROJ_PATH}/scripts/try_collector.sh

# Allow user to assign venv name and tag shell prompt
export ML_VENV_NAME=${ML_VENV_NAME:-ml-venv-${PY_VER}-dld}
export PS1_TAG="(${ML_VENV_NAME}) "
export PS1="${PS1_TAG}${PS1:-\$ }"

# Run the environment
docker run -ti --rm \
  -u $(id -u):$(id -g) \
  -v ${PROJ_PATH}:/work -w /work \
  -e PIP_ARGS="--no-index --find-links /work/pip_pkgs/${PY_VER}" \
  -e HOME=/work \
  -e ML_VENV_NAME="${ML_VENV_NAME}" \
  -e PY_VER="${PY_VER}" \
  -e PS1_TAG="${PS1_TAG}" \
  -e PS1="${PS1}" \
  python:${PY_VER}-slim \
  /work/scripts/build-dev-venv.sh
