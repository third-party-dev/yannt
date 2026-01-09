#!/usr/bin/env bash

PROJ_PATH=$(realpath $(dirname $0)/..)
PY_VER=${PY_VER:-$(python3 --version | awk '{print $2}' | cut -d. -f1,2)}

# Detect if we can run the collector
# BUG: Logic should be reversed so we know _all_ URLs work.
CAN_ACCESS_UPSTREAM=${CAN_ACCESS_UPSTREAM:-false}
for url in https://download.pytorch.org/whl/cpu https://pypi.org/simple; do
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

# Default to using system python version. Expecting only major.minor (e.g 3.13)
mkdir -p ${PROJ_PATH}/pip_pkgs/${PY_VER}

DEFAULT_PIP_ARGS="
  --index-url https://download.pytorch.org/whl/cpu \
  --extra-index-url https://pypi.org/simple
"

PIP_ARGS=${PIP_ARGS:-${DEFAULT_PIP_ARGS}}

# Download CPU-only Torch and everything else
docker run -ti --rm \
  -v ${PROJ_PATH}:/work -w /work/pip_pkgs/${PY_VER} \
  -e PIP_ARGS="$PIP_ARGS" \
  -e HOME=/work \
  -u $(id -u):$(id -g) \
  python:${PY_VER}-slim \
  /work/scripts/download_deps_for.sh \
    /work/yannt \
    /work/extern/thirdparty_pparse \
    /work/extern/thirdparty_yannt_transformers
