#!/usr/bin/env bash

#sudo apt install python3.13-venv
#sudo apt install python3-argcomplete
#sudo apt install python3-pip

set -e

# TODO: What does no target do?

# Load environment configuration
source ${CONFIG_PATH}/config


if [ "${RUN_MODE}" = "build" ]; then
  echo "Building the venv."
  CONTAINER_CMD=${CRI_PROJ_PATH}/scripts/_build-venv.sh
else
  echo "Starting the venv."
  if [ ! -e "${PROJ_PATH}/cache/venv/${ML_VENV_NAME}" ]; then
    # If we're running an environment that doesn't exist, stop.
    echo "You are attempting to run an environment that doesn't exist. (${ML_VENV_NAME})"
    echo "Run: ./scripts/init-dev.sh ${CONFIG_NAME}"
    exit 1
  fi
  CONTAINER_CMD=${CRI_PROJ_PATH}/scripts/_start-venv.sh
fi


# Run the environment
mkdir -p ${PROJ_PATH}/cache/docker-home

docker run -ti --rm \
    -u $(id -u):$(id -g) \
    -v ${PROJ_PATH}:${CRI_PROJ_PATH} \
    -w ${CRI_PROJ_PATH} \
    -e CRI_PROJ_PATH="${CRI_PROJ_PATH}" \
    -e PY_VER="${PY_VER}" \
    -e PY_REQS="${PY_REQS}" \
    -e PY_CONSTRAINTS="${PY_CONSTRAINTS}" \
    -e HOME=${CRI_PROJ_PATH}/cache/docker-home \
    -e USER="user" \
    -e ML_VENV_NAME="${ML_VENV_NAME}" \
    ml-venv-dev:${PY_VER}-slim \
    ${CONTAINER_CMD}