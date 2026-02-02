#!/usr/bin/env bash

#sudo apt install python3.13-venv
#sudo apt install python3-argcomplete
#sudo apt install python3-pip

set -e

# TODO: Check if PY_VER is set.

PROJ_PATH=$(realpath $(dirname $0)/..)

export PY_VER=${PY_VER:-$(python3 --version | awk '{print $2}' | cut -d. -f1,2)}
export PY_CONSTRAINTS=${PY_CONSTRAINTS:-}

# Allow user to assign venv name and tag shell prompt
export ML_VENV_NAME=${ML_VENV_NAME:-ml-venv-${PY_VER}-dld}
export PS1_TAG="(${ML_VENV_NAME}) "
export PS1="${PS1_TAG}${PS1:-\$ }"

mkdir -p ${PROJ_PATH}/scripts/context
docker build -t init-docker-local-dev:${PY_VER}-slim --build-arg PY_VER="${PY_VER}" \
  -f ${PROJ_PATH}/scripts/init-docker-local-dev.dockerfile \
  ${PROJ_PATH}/scripts/context

[ -z "$SKIP_COLLECT" ] && ${PROJ_PATH}/scripts/try_collector.sh

./scripts/run-docker-local-dev.sh
