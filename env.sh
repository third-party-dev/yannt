#!/usr/bin/env bash

EXTERN_DIR="./extern"

ARG1="$1"

export PS1_TAG="(ml-venv) "
export PS1="${PS1_TAG}${PS1:-\$ }"

PIP_INSTALL_FLAGS=""
TORCH_FLAGS="--index-url https://download.pytorch.org/whl/cpu"
if [ "$ARG1" == "offline" ]; then
  PIP_INSTALL_FLAGS="--no-index --find-links docker/context/pip_pkgs"
  TORCH_FLAGS=""
fi

if [ ! -e "./ml-venv" ]; then
  python3 -m venv ./ml-venv
  [ $? -ne 0 ] && { echo "Failed to create venv"; exit 1; }
  ./ml-venv/bin/pip install --upgrade $PIP_INSTALL_FLAGS pip setuptools wheel build pytest
fi
source ./ml-venv/bin/activate

# TODO: These dependencies should be managed by pyproject.toml.
echo Checking dependencies.
pip show pytest &>/dev/null || pip install $PIP_INSTALL_FLAGS pytest
pip show protobuf &>/dev/null || pip install $PIP_INSTALL_FLAGS protobuf
pip show numpy &>/dev/null || pip install $PIP_INSTALL_FLAGS numpy
pip show transformers &>/dev/null || pip install $PIP_INSTALL_FLAGS transformers
pip show torch &>/dev/null || pip install $PIP_INSTALL_FLAGS torch $TORCH_FLAGS

# TODO: Do we always want to install? Do we track md5 of pyproject.toml?
pip show thirdparty_yannt &>/dev/null || pip install -e yannt

# pip install for each extern
mkdir -p "$EXTERN_DIR"
for pkgpath in "$EXTERN_DIR"/*; do
  if [ -d "$pkgpath" ]; then
    pip show $(basename "$pkgpath") &>/dev/null || pip install -e $pkgpath
  fi
done

echo
echo  "The environment is now ready. Try 'yannt --help' for information."

exec bash -i
