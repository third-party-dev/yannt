#!/usr/bin/env bash

set -e

# --------- Guard Against Uninitialized Environments -------

if [ -z "${PROJ_PATH}" ]; then
  echo "Please run via ./scripts/run-dev.sh."
  exit 1
fi

source ${CONFIG_PATH}/config.env

${PROJ_PATH}/cache/builder/${CONFIG_NAME}/host/conda/run-conda.sh