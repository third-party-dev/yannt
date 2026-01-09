#!/usr/bin/env bash

PROJ_PATH=$(realpath $(dirname $0)/..)
export PY_VER=${PY_VER:-$(python3 --version | awk '{print $2}' | cut -d. -f1,2)}

# Allow user to assign venv name and tag shell prompt
export ML_VENV_NAME=${ML_VENV_NAME:-ml-venv-${PY_VER}-hld}
export PS1_TAG="(${ML_VENV_NAME}) "
export PS1="${PS1_TAG}${PS1:-\$ }"

# Default to using system python version. Expecting only major.minor (e.g 3.13)
[ -z "$SKIP_COLLECT" ] && ${PROJ_PATH}/scripts/try_collector.sh

# Do the local install
PIP_ARGS="--no-index --find-links pip_pkgs/${PY_VER}" \
  ${PROJ_PATH}/scripts/build-dev-venv.sh
