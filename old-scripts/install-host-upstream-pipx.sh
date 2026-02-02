#!/usr/bin/env bash

PROJ_PATH=$(realpath $(dirname $0)/..)
export PY_VER=${PY_VER:-$(python3 --version | awk '{print $2}' | cut -d. -f1,2)}

if [ ! -e "${PROJ_PATH}/pip_pkgs/yannt/${PY_VER}" ]; then
    echo "You must prestage packages in ${PROJ_PATH}/pip_pkgs/yannt/${PY_VER}."
    echo "Have you built the project? \`./scripts/build-docker-local-prod.sh\`"
    exit 1
fi

export PIP_ARGS="
  --find-links=${PROJ_PATH}/pip_pkgs/yannt/${PY_VER} \
  --index-url https://download.pytorch.org/whl/cpu \
  --extra-index-url https://pypi.org/simple
"

pipx install --pip-args "${PIP_ARGS}" thirdparty_yannt
pipx inject thirdparty_yannt --pip-args "${PIP_ARGS}" thirdparty_pparse
pipx inject thirdparty_yannt --pip-args "${PIP_ARGS}" thirdparty_yannt_transformers
