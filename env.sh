#!/usr/bin/env bash

EXTERN_DIR="./extern"

# Required for developer container
ML_VENV_NAME=${ML_VENV_NAME:-ml-venv}

ARG1="$1"

export PS1_TAG="(${ML_VENV_NAME}) "
export PS1="${PS1_TAG}${PS1:-\$ }"

# TODO: Consider other options for dev container build
cd docker; ./download.sh; cd ..

PIP_INSTALL_FLAGS="--no-index --find-links docker/context/pip_pkgs"

if [ ! -e "./${ML_VENV_NAME}" ]; then
  python3 -m venv ./${ML_VENV_NAME}
  [ $? -ne 0 ] && { echo "Failed to create venv"; exit 1; }
  ./${ML_VENV_NAME}/bin/pip install --upgrade $PIP_INSTALL_FLAGS pip setuptools wheel build pytest
fi
source ./${ML_VENV_NAME}/bin/activate

# TODO: These dependencies should be managed by pyproject.toml.
echo Checking dependencies.

pip show thirdparty_yannt &>/dev/null || pip install $PIP_INSTALL_FLAGS -e yannt

# pip install for each extern
mkdir -p "$EXTERN_DIR"
for pkgpath in "$EXTERN_DIR"/*; do
  if [ -d "$pkgpath" ]; then
    pip show $(basename "$pkgpath") &>/dev/null || pip install $PIP_INSTALL_FLAGS -e $pkgpath
  fi
done

echo
echo  "The environment is now ready. Try 'yannt --help' for information."

exec bash -i
