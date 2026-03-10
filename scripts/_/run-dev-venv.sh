#!/usr/bin/env bash

#sudo apt install python3.13-venv
#sudo apt install python3-argcomplete
#sudo apt install python3-pip

set -e

# TODO: What does no target do?

# Load environment configuration
source ${CONFIG_PATH}/config


if [ -n "${BUILD_MODE}" ]; then
  echo "Building the venv."
  ${PROJ_PATH}/scripts/_/build-venv.sh $@
else
  echo "Starting the venv."
  if [ ! -e "${PROJ_PATH}/cache/venv/${ML_VENV_NAME}" ]; then
    # If we're running an environment that doesn't exist, stop.
    echo "You are attempting to run an environment that doesn't exist. (${ML_VENV_NAME})"
    echo "Run: ./scripts/init-dev.sh ${CONFIG_NAME}"
    exit 1
  fi
  ${PROJ_PATH}/scripts/_/start-venv.sh $@
fi

