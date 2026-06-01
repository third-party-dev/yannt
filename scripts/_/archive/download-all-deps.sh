#!/bin/sh

# !! Note: This script is intended to be run from inside a docker container.

# Vars needed to be passed:
# - PY_CONSTRAINTS
# - PY_REQS
# - PIP_IDX_ARGS
# - PY_VER
# - 

# Assuming we're in the top level yannt folder regardless of CRI or host.

PY_CONSTRAINTS=${PY_CONSTRAINTS:-}
if [ -n "${PY_CONSTRAINTS}" ]; then
    PY_CONSTRAINTS_ARGS="-c ${PY_CONSTRAINTS}"
else
    PY_CONSTRAINTS_ARGS=
fi

PY_REQS=${PY_REQS:-}
if [ -n "${PY_REQS}" ]; then
    PY_REQS_ARGS="-r ${PY_REQS}"
else
    PY_REQS_ARGS=
fi

PIP_DL_ARGS=${PIP_DL_ARGS:-"${PIP_IDX_ARGS} -d ./cache/pip_pkgs/${PY_VER}"}
PYTHON=${PYTHON:-"python"}
PIP=${PIP:-"${PYTHON} -m pip"}

# $(${PIP} 2>/dev/null)
# if [ $? -ne 0 ]; then
#   echo "ERROR: It appears that pip is not installed for ${PYTHON}"
#   echo
#   echo "If you are running on an apt based system, this can usually"
#   echo "be fixed with:"
#   echo
#   echo "  apt-get install python3-pip"
#   echo
#   echo "Note: Your environment's python version is $(python3 --version)"
#   exit 1
# fi

mkdir -p ./cache/pip_pkgs/${PY_VER}

echo PIP_DL_ARGS: ${PIP_DL_ARGS}
echo PIP DOWNLOAD: ${PIP} download ${PIP_DL_ARGS} ${PY_REQS_ARGS} ${PY_CONSTRAINTS_ARGS}
${PIP} download ${PIP_DL_ARGS} ${PY_REQS_ARGS} ${PY_CONSTRAINTS_ARGS}

PKG_SKIP_LIST=${PKG_SKIP_LIST:-""}

# Do enabled python packages
for ext in `ls -1 ./configs/auto_install`; do

    skip=0
    for blocked in $PKG_SKIP_LIST; do
        if [ "$ext" = "$blocked" ]; then
            skip=1
            break
        fi
    done
    if [ "$skip" = "1" ]; then
        echo "Skipping $ext."
        continue
    fi

    ${PIP} download ${PIP_DL_ARGS} ${PY_CONSTRAINTS_ARGS} ./configs/auto_install/$ext
done

