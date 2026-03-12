#!/usr/bin/env bash

set -e

# --------- Guard Against Uninitialized Environments -------

if [ -z "${PROJ_PATH}" ]; then
  echo "Please run via ./scripts/init-dev.sh."
  exit 1
fi

mkdir -p ${CRI_ROOT}

# Forward to generic script.
${PROJ_PATH}/scripts/_/init-dev-venv.sh $@