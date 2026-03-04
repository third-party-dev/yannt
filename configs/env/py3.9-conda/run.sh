#!/usr/bin/env bash

set -e

# --------- Guard Against Uninitialized Environments -------

if [ -z "${PROJ_PATH}" ]; then
  echo "Please run via ./scripts/run-dev.sh."
  exit 1
fi

# Forward to generic script.
${PROJ_PATH}/scripts/_run-dev-conda.sh $@

