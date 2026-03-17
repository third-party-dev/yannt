#!/usr/bin/env bash

# The following should be set:
# PROJ_PATH - Full path to yannt
# CONFIG_NAME - Name of config folder
# CONFIG_PATH - Full path to config folder

# Load environment configuration
source ${CONFIG_PATH}/config

# Check if given python is in path.
PYTHON=${PYTHON:-python}
if [ -z "$(which ${PYTHON})" ]; then
  echo "Could not locate ${PYTHON}. Please add ${PYTHON} to PATH."
  echo 
  echo "  Example: export PATH=\$PATH:/opt/${PYTHON}/bin"
  echo
  echo "To install from upstream you can try to find a package from:"
  echo
  echo "  https://github.com/astral-sh/python-build-standalone/releases"
  echo
  echo " or"
  echo
  echo "  apt-get install pipx        # Ensure pipx is installed."
  echo "  pipx install pystand        # Ensure pystand is installed"
  echo "  pystand show                # Show architecture matching versions"
  echo "  pystand install ${PY_VER}   # Install python version"
  echo "  export PATH=\$PATH:$(pystand path)/${PY_VER}/bin"
  echo
  exit 1
fi

# Construct the base container image (venv created from container runtime)
mkdir -p ${PROJ_PATH}/cache/venv

# ----- Fetch and cache python deps ----

if [ -z "$SKIP_COLLECT" ]; then

  if [ -n "$PIP_UPSTREAM_VERIFIERS" ]; then
    # Detect if we can run the collector
    # BUG: Logic should be reversed so we know _all_ URLs work.
    CAN_ACCESS_UPSTREAM=${CAN_ACCESS_UPSTREAM:-false}
    for url in ${PIP_UPSTREAM_VERIFIERS}; do
        if curl -fsI "$url" >/dev/null 2>&1; then
            CAN_ACCESS_UPSTREAM=true
            break
        fi
    done
    if [ "$CAN_ACCESS_UPSTREAM" = false ]; then
        echo "No internet detected."
        echo "Assuming deps in: ${PROJ_PATH}/pip_pkgs/${PY_VER}"
        exit 0
    fi
  fi

  mkdir -p ${PROJ_PATH}/cache/pip_pkgs/${PY_VER}

  ${PROJ_PATH}/scripts/_/download-all-deps.sh
  if [ $? -ne 0 ]; then
    echo "download-all-deps.sh failed. Stopping now."
    exit 1
  fi

fi

BUILD_MODE="build" ${PROJ_PATH}/scripts/run-dev.sh ${CONFIG_NAME}