#!/usr/bin/env bash

set -e

# --------- Guard Against Uninitialized Environments -------

if [ -z "${PROJ_PATH}" ]; then
  echo "Please run via ./scripts/init-dev.sh."
  exit 1
fi

# The following should be set:
# PROJ_PATH - Full path to yannt
# CONFIG_NAME - Name of config folder
# CONFIG_PATH - Full path to config folder

# -------- Initialize CONDA Environment ---------

# Load environment configuration
source ${CONFIG_PATH}/config

# Attempt to activate conda
CRI_BIN_ONLY=$(echo "${CRI_BIN}" | cut -d ' ' -f 1)
if [ -z "$(which ${CRI_BIN_ONLY})" ]; then
  echo "Could not locate ${CRI_BIN_ONLY} (CRI_BIN). Please add ${CRI_BIN_ONLY} to PATH."
  echo 
  echo "  Example: export PATH=\$PATH:/opt/${CRI_BIN_ONLY}/bin"
  echo
  exit 1
fi

# Note: Assuming it is OK to not check if the environment exists.

if [ -n "${NO_SHELL}" ]; then
  CRI_CMD="bash -c 'exit'"
else
  CRI_CMD=${CRI_CMD:-"$@"}
  echo CRI_CMD ${CRI_CMD}
fi

# Run the environment
mkdir -p ${PROJ_PATH}/cache/docker-home

${CRI_BIN} run -ti --rm \
    -u $(id -u):$(id -g) \
    -v ${PROJ_PATH}:${CRI_PROJ_PATH} \
    -w ${CRI_PROJ_PATH} \
    -e CRI_PROJ_PATH="${CRI_PROJ_PATH}" \
    -e HOME=${CRI_PROJ_PATH}/cache/docker-home \
    -e USER="user" \
    ${CRI_RUN_ARGS} \
    docker.io/ultralytics/ultralytics:8.4.8-python-export \
    ${CRI_CMD}