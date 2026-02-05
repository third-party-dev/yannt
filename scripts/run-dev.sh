#!/usr/bin/env bash

#sudo apt install python3.13-venv
#sudo apt install python3-argcomplete
#sudo apt install python3-pip

set -e

export PROJ_PATH=${PROJ_PATH:-$(realpath $(dirname $0)/..)}
export CONFIG_NAME="$1"
export RUN_MODE="$2"
export CONFIG_PATH="${PROJ_PATH}/configs/env/${CONFIG_NAME}"

if [ -z "$CONFIG_NAME" -o "$CONFIG_NAME" = "list" ]; then
    ls -1 ${PROJ_PATH}/configs/env
    exit 0
fi

if [ ! -e "${CONFIG_PATH}" ]; then
    echo "Could not find config file for ${CONFIG_NAME}"
    exit 1
fi

# TODO: What does no target do?

# Load environment configuration
source ${CONFIG_PATH}/config


if [ "${RUN_MODE}" = "build" ]; then
  echo "Building the venv."
  CONTAINER_CMD=/work/scripts/build-venv.sh
else
  if [ ! -e "${PROJ_PATH}/cache/venv/${ML_VENV_NAME}" ]; then
    # If we're running an environment that doesn't exist, stop.
    echo "You are attempting to run an environment that doesn't exist. (${ML_VENV_NAME})"
    echo "Run: ./scripts/init-dev.sh ${CONFIG_NAME}"
    exit 1
  fi
  CONTAINER_CMD=/work/scripts/start-venv.sh
fi


# Run the environment
docker run -ti --rm \
    -u $(id -u):$(id -g) \
    -v ${PROJ_PATH}:/work -w /work \
    -e PIP_ARGS="--no-index --find-links /work/cache/pip_pkgs/${PY_VER}" \
    -e PY_CONSTRAINTS="${PY_CONSTRAINTS}" \
    -e HOME=/work/cache \
    -e ML_VENV_NAME="${ML_VENV_NAME}" \
    -e PY_VER="${PY_VER}" \
    -e PIP_PKGS="${PIP_PKGS}" \
    ml-venv-dev:${PY_VER}-slim \
    ${CONTAINER_CMD}
