#!/usr/bin/env bash

# The following should be set:
# PROJ_PATH - Full path to yannt
# CONFIG_NAME - Name of config folder
# CONFIG_PATH - Full path to config folder

# Load environment configuration
source ${CONFIG_PATH}/config

# # TODO: Make this configurable?
# export PS1="${PS1_TAG}${PS1:-\$ }"

# TODO: Do we construct ARGS for constraints and requirements here?

# Construct the base container image (venv created from container runtime)
mkdir -p ${PROJ_PATH}/cache/empty-context
docker build \
  -t ml-venv-dev:${PY_VER}-slim \
  --build-arg PY_VER="${PY_VER}" \
  --build-arg APT_PKGS="${APT_PKGS}" \
  -f ${PROJ_PATH}/scripts/init-dev.dockerfile \
  ${PROJ_PATH}/cache/empty-context


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
  mkdir -p ${PROJ_PATH}/cache/docker-home

  docker run -ti --rm \
    -v ${PROJ_PATH}:${CRI_PROJ_PATH} \
    -w ${CRI_PROJ_PATH} \
    -e PY_REQS="$PY_REQS" \
    -e PY_CONSTRAINTS="${PY_CONSTRAINTS}" \
    -e PIP_IDX_ARGS="$PIP_IDX_ARGS" \
    -e PY_VER="$PY_VER" \
    -e USER="user" \
    -e HOME=${CRI_PROJ_PATH}/cache/docker-home \
    -u $(id -u):$(id -g) \
    ml-venv-dev:${PY_VER}-slim \
    ${CRI_PROJ_PATH}/scripts/_download-all-deps.sh

fi

${PROJ_PATH}/scripts/run-dev.sh ${CONFIG_NAME} build