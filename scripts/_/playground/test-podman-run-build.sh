#!/usr/bin/env bash

CRI_BIN="podman --root $(pwd)/cache/podman-runroot"
PY_VER=3.11
ML_VENV_NAME=test-py${PY_VER}-podman
CRI_RUN="${CRI_BIN} exec ${ML_VENV_NAME}"

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

# Check if container already exists and ensure user is ok with restarting.
RESULT=$(PODMAN ps -a --filter "name=${ML_VENV_NAME}" --format "{{.Names}}")
if [ -n "${RESULT}" ]; then
    echo "Container ${ML_VENV_NAME} exists."

    echo -n "Stop and remove existing container? (y/n) "
    read answer

    case "$answer" in
        [Yy]*)
            PODMAN stop $ML_VENV_NAME
            if [ $? -ne 0 ]; then
                echo "Failed to stop container. Cancelling."
                exit 1
            fi
            PODMAN rm $ML_VENV_NAME
            if [ $? -ne 0 ]; then
                echo "Failed to rm container. Cancelling."
                exit 1
            fi
            ;;
        [Nn]*)
            echo "Cancelled. To do it manually:"
            echo
            echo "${CRI_BIN} stop ${ML_VENV_NAME}"
            echo "${CRI_BIN} rm ${ML_VENV_NAME}"
            ;;
        *)
            echo "Invalid response. Cancelling."
            ;;
    esac
fi

echo "Creating container ${ML_VENV_NAME}"

CONTAINER=$(\
  PODMAN create --name $ML_VENV_NAME \
    -u 0:0 --userns=keep-id \
    -v $(pwd):/work/cache/docker-home -w /work \
    -e PY_VER=${PY_VER} -e HOME=/work \
    docker.io/library/python:${PY_VER}-slim \
    tail -f /dev/null
)

echo "Created container ${ML_VENV_NAME}@${CONTAINER}"

PODMAN start $CONTAINER
if [ $? -ne 0 ]; then
    echo "Failed to start container. Cancelling."
    exit 1
fi

echo "Started ${ML_VENV_NAME}@${CONTAINER}"

RUN chown root /var/lib/apt/lists/partial
RUN chfsown root /var/lib/apt/lists/auxfiles
RUN chown root /var/cache/apt/archives/partial
RUN chown root /var/log/apt

RUN apt-get update
RUN apt-get install -y vim unzip
RUN useradd -m user

echo "Saving container as localhost/${ML_VENV_NAME}"

PODMAN commit ${ML_VENV_NAME} localhost/${ML_VENV_NAME}