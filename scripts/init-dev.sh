#!/usr/bin/env bash

set -e

export PROJ_PATH=$(realpath $(dirname $0)/..)
export CONFIG_NAME="$1"
export CONFIG_PATH="${PROJ_PATH}/configs/env/${CONFIG_NAME}"

if [ "$CONFIG_NAME" = "list" ]; then
    ls -1 ${PROJ_PATH}/configs/env
    exit 0
fi

if [ ! -e "${CONFIG_PATH}/config" ]; then
    echo "Could not find config file for ${CONFIG_NAME}"
    exit 1
fi

# TODO: What does no target do?

# Load environment configuration
source ${CONFIG_PATH}/config

# TODO: Make this configurable?
export PS1="${PS1_TAG}${PS1:-\$ }"

# TODO: Do we construct ARGS for contraints and requirements here?

# Construct the container image
mkdir -p ${PROJ_PATH}/cache/empty-context
docker build \
  -t ml-venv-dev:${PY_VER}-slim \
  --build-arg PY_VER="${PY_VER}" \
  --build-arg APT_PKGS="${APT_PKGS}" \
  -f ${PROJ_PATH}/scripts/init-dev.dockerfile \
  ${PROJ_PATH}/cache/empty-context

# Populate pip_pkgs
[ -z "$SKIP_COLLECT" ] && ${PROJ_PATH}/scripts/try-collector.sh

${PROJ_PATH}/scripts/run-dev.sh ${CONFIG_NAME} build
