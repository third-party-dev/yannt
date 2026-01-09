#!/usr/bin/env bash

# TODO: Check if PY_VER is set.

PROJ_PATH=$(realpath $(dirname $0)/..)

# Detect if we can run the collector
CAN_ACCESS_UPSTREAM=false
for url in https://download.pytorch.org/whl/cpu https://pypi.org/simple; do
    if curl -fsI "$url" >/dev/null 2>&1; then
        CAN_ACCESS_UPSTREAM=true
        break
    fi
done

if [ "$CAN_ACCESS_UPSTREAM" = true ]; then
    # Collect the dependencies
    ${PROJ_PATH}/scripts/collector.sh
fi

# Allow user to assign venv name and tag shell prompt
export ML_VENV_NAME=${ML_VENV_NAME:-ml-venv}
export PS1_TAG="(${ML_VENV_NAME}) "
export PS1="${PS1_TAG}${PS1:-\$ }"

# Run the environment
docker run -ti --rm \
  -u $(id -u):$(id -g) \
  -v ${PROJ_PATH}:/work -w /work \
  -e PIP_ARGS="--no-index --find-links /work/pip_pkgs/${PY_VER}" \
  -e HOME=/work \
  python:${PY_VER:-3.13}-slim \
  /work/scripts/build-dev-venv.sh
