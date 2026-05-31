#!/usr/bin/env bash

#echo RUNNING BUILD_MODE="${BUILD_MODE}" PROJ_PATH="${PROJ_PATH}" $0 $@

set -e

# --------- Guard Against Uninitialized Environments -------

if [ -z "${PROJ_PATH}" ]; then
  echo "Please run via ./scripts/run-dev.sh."
  exit 1
fi

${PROJ_PATH}/cache/builder/${CONFIG_NAME}/host/podman/run-podman.sh



