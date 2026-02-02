#!/usr/bin/env bash

PROJ_PATH=$(realpath $(dirname $0)/..)

EXTERN_DIR=${PROJ_PATH}/extern

# Allow user to assign venv name and tag shell prompt
ML_VENV_NAME=${ML_VENV_NAME:-ml-venv}
export PS1_TAG="(${ML_VENV_NAME}) "
export PS1="${PS1_TAG}${PS1:-\$ }"

# Assuming we've already collected.

mkdir -p ${PROJ_PATH}/venv
if [ ! -e "${PROJ_PATH}/venv/${ML_VENV_NAME}" ]; then
  python3 -m venv ${PROJ_PATH}/venv/${ML_VENV_NAME}
  [ $? -ne 0 ] && { echo "Failed to create venv"; exit 1; }
  echo "--------------------- Setting Up Base Python Requirements ---------------------"
  ${PROJ_PATH}/venv/${ML_VENV_NAME}/bin/pip install --upgrade $PIP_ARGS pip setuptools wheel build pytest
fi
source ${PROJ_PATH}/venv/${ML_VENV_NAME}/bin/activate

mkdir -p ${PROJ_PATH}/pip_pkgs/yannt/${PY_VER}

cd ${PROJ_PATH}/yannt
python -m build --sdist
python -m build --wheel
cp dist/* ${PROJ_PATH}/pip_pkgs/yannt/${PY_VER}/


# pip install for each extern
mkdir -p ${EXTERN_DIR}
for pkgpath in ${EXTERN_DIR}/*; do
  if [ -d "$pkgpath" ]; then
    echo "------ BUILDING: $pkgpath ------"
    cd $pkgpath
    python -m build --sdist
    python -m build --wheel
    cp dist/* ${PROJ_PATH}/pip_pkgs/yannt/${PY_VER}/
  fi
done
