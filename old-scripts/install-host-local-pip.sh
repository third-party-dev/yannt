#!/usr/bin/env bash

PROJ_PATH=$(realpath $(dirname $0)/..)
export PY_VER=${PY_VER:-$(python3 --version | awk '{print $2}' | cut -d. -f1,2)}

# if [ ! -e "${PROJ_PATH}/pip_pkgs/yannt/${PY_VER}" ]; then
#     echo "You must prestage packages in ${PROJ_PATH}/pip_pkgs/yannt/${PY_VER}."
#     echo "Have you built the project? \`./scripts/build-docker-local-prod.sh\`"
#     exit 1
# fi

# For good measure, go ahead and try collection again.
[ -z "$SKIP_COLLECT" ] && ${PROJ_PATH}/scripts/try_collector.sh

export PIP_ARGS="
  -U --no-index \
  --find-links=${PROJ_PATH}/pip_pkgs/yannt/${PY_VER} \
  --find-links=${PROJ_PATH}/pip_pkgs/${PY_VER}
"

pip uninstall -y thirdparty_yannt
pip uninstall -y thirdparty_pparse
pip uninstall -y thirdparty_yannt_transformers

pip install ${PIP_ARGS} thirdparty_yannt
pip install ${PIP_ARGS} thirdparty_pparse
pip install ${PIP_ARGS} thirdparty_yannt_transformers
