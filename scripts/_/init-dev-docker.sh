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
${CRI_BIN} build \
  -t localhost/${ML_VENV_NAME} \
  --build-arg PY_VER="${PY_VER}" \
  --build-arg APT_PKGS="${APT_PKGS}" \
  -f ${PROJ_PATH}/scripts/_/init-dev.dockerfile \
  ${PROJ_PATH}/cache/empty-context


# ----- Fetch and cache python deps ----

if [ -z "$SKIP_COLLECT" ]; then

  if [ -n "$(echo ${PIP_UPSTREAM_VERIFIERS} | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')" ]; then
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
  mkdir -p ${PROJ_PATH}/${CRI_HOME}

  ${CRI_BIN} run -ti --rm \
    -v ${PROJ_PATH}:${CRI_PROJ_PATH} \
    -w ${CRI_PROJ_PATH} \
    -e CRI_PROJ_PATH="${CRI_PROJ_PATH}" \
    -e PY_REQS="$PY_REQS" \
    -e PY_CONSTRAINTS="${PY_CONSTRAINTS}" \
    -e PIP_IDX_ARGS="${PIP_IDX_ARGS}" \
    -e PY_VER="$PY_VER" \
    -e USER="user" \
    -e HOME=${CRI_PROJ_PATH}${CRI_HOME} \
    -u $(id -u):$(id -g) \
    ${CRI_RUN_ARGS} \
    localhost/${ML_VENV_NAME} \
    ${CRI_PROJ_PATH}/scripts/_/download-all-deps.sh

fi

BUILD_MODE="build" ${PROJ_PATH}/scripts/run-dev.sh ${CONFIG_NAME}