#!/usr/bin/env bash

PROJ_PATH=$(realpath $(dirname $0)/..)

# Allow user to assign venv name and tag shell prompt
export ML_VENV_NAME=${ML_VENV_NAME:-ml-venv}
export PS1_TAG="(${ML_VENV_NAME}) "
export PS1="${PS1_TAG}${PS1:-\$ }"

# Default to using system python version. Expecting only major.minor (e.g 3.13)
PIP_ARGS="
  --index-url https://download.pytorch.org/whl/cpu \
  --extra-index-url https://pypi.org/simple
" ${PROJ_PATH}/scripts/collector.sh

# Do the local install
PIP_ARGS="--no-index --find-links pip_pkgs/${PY_VER}" \
  ${PROJ_PATH}/scripts/build-dev-venv.sh
