#!/usr/bin/env bash

# The following should be set:
# PROJ_PATH - Full path to yannt
# CONFIG_NAME - Name of config folder
# CONFIG_PATH - Full path to config folder

# Load environment configuration
source ${CONFIG_PATH}/config

mkdir -p ${CRI_ROOT}

# ------------- Podman Hackery ------------

PODMAN() {
    ${CRI_BIN} $@
    if [ $? -ne 0 ]; then
        echo "Failed to run: $@"
        echo "Cancelling."
        exit 1
    fi
}

RUN() {
    ${CRI_RUN} $@
    if [ $? -ne 0 ]; then
        echo "Failed to run: $@"
        echo "Cancelling."
        exit 1
    fi
}

BUILD_CONTAINER() {
    # Initial stop and rm allowed to fail.
    ${CRI_BIN} stop $ML_VENV_NAME
    ${CRI_BIN} rm $ML_VENV_NAME

    echo "Creating container ${ML_VENV_NAME}"
    CONTAINER=$(\
    ${CRI_BIN} create --name $ML_VENV_NAME \
        -v $(pwd):/work/cache/docker-home -w /work \
        -e PY_VER=${PY_VER} -e HOME=/work \
        ${CRI_RUN_ARGS} \
        docker.io/library/python:${PY_VER}-slim \
        tail -f /dev/null
    )
    echo "Created container ${ML_VENV_NAME}@${CONTAINER}"

    PODMAN start $CONTAINER
    echo "Started ${ML_VENV_NAME}@${CONTAINER}"

    RUN chown root /var/lib/apt/lists/partial
    RUN chown root /var/lib/apt/lists/auxfiles
    RUN chown root /var/cache/apt/archives/partial
    RUN chown root /var/log/apt

    RUN apt-get -o APT::Sandbox::User=root update
    RUN apt-get -o APT::Sandbox::User=root install -y vim unzip ${APT_PKGS}
    RUN useradd -m user

    echo "Saving container as localhost/${ML_VENV_NAME}"
    PODMAN commit ${ML_VENV_NAME} localhost/${ML_VENV_NAME}
    echo "Committed \(i.e. saved\) ${ML_VENV_NAME}@${CONTAINER} image."

    PODMAN stop ${ML_VENV_NAME}
    echo "Stopped ${ML_VENV_NAME}@${CONTAINER}"
}

# Check if container already exists and ensure user is ok with restarting.
RESULT=$(${CRI_BIN} ps -a --filter "name=${ML_VENV_NAME}" --format "{{.Names}} 2>/dev/null")
if [ -n "${RESULT}" ]; then
    echo "Container ${ML_VENV_NAME} exists."
    echo
    echo -n "[R]ebuild container, [s]kip build, or [a]bort? (r/s/a) "
    read answer

    case "$answer" in
        [Rr]*)
            BUILD_CONTAINER
            ;;
        [Ss]*)
            echo "Using the existing container image."
            ;;
        *)
            echo "Aborting the process."
            exit 1
            ;;
    esac
else
    echo "Existing container not found. Building now."
    BUILD_CONTAINER
fi

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
    -e HOME=${CRI_PROJ_PATH}/${CRI_HOME} \
    -u $(id -u):$(id -g) \
    ${CRI_RUN_ARGS} \
    localhost/${ML_VENV_NAME} \
    ${CRI_PROJ_PATH}/scripts/_/download-all-deps.sh

fi

BUILD_MODE="build" ${PROJ_PATH}/scripts/run-dev.sh ${CONFIG_NAME}