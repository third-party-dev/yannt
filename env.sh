#!/usr/bin/env bash

EXTERN_DIR="./extern"

export PS1_TAG="(ml-venv) "
export PS1="${PS1_TAG}${PS1:-\$ }"

if [ ! -e "./ml-venv" ]; then
  python3 -m venv ./ml-venv
  [ $? -ne 0 ] && { echo "Failed to create venv"; exit 1; }
  ./ml-venv/bin/pip install --upgrade pip setuptools wheel build pytest
fi
source ./ml-venv/bin/activate

# TODO: These dependencies should be managed by pyproject.toml.
echo Checking dependencies.
pip show pytest &>/dev/null || pip install pytest
pip show protobuf &>/dev/null || pip install protobuf
pip show numpy &>/dev/null || pip install numpy
pip show transformers &>/dev/null || pip install transformers
pip show torch &>/dev/null || pip install torch --index-url https://download.pytorch.org/whl/cpu

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
