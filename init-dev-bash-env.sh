#!/usr/bin/env bash

SCRIPT_PATH=$(realpath $(dirname $0))

EXTERN_DIR="./extern"

# Default to using system python version. Expecting only major.minor (e.g 3.13)
PY_VER=${PY_VER:-$(python3 --version | awk '{print $2}' | cut -d. -f1,2)}

# Allow user to assign venv name and tag shell prompt
ML_VENV_NAME=${ML_VENV_NAME:-ml-venv}
export PS1_TAG="(${ML_VENV_NAME}) "
export PS1="${PS1_TAG}${PS1:-\$ }"

mkdir -p ${SCRIPT_PATH}/pip_pkgs/${PY_VER}

# Download CPU-only Torch and everything else
docker run -ti --rm \
  -v ${SCRIPT_PATH}:/work -w /work/pip_pkgs/${PY_VER} \
  python:${PY_VER}-slim \
  /work/scripts/download_deps_for.sh \
    /work/yannt \
    /work/extern/thirdparty_pparse \
    /work/extern/thirdparty_yannt_transformers

exit 0
# TODO: Consider other options for dev container build
#cd docker; ./download.sh; cd ..

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
    pip show $(basename "$pkgpath") &>/dev/null || pip install -U $PIP_INSTALL_FLAGS -e $pkgpath
  fi
done

echo
echo "The environment is now ready. Try 'yannt --help' for information."

# Include yannt tab completion.
TMP_RC="$(mktemp)"
cat >> "$TMP_RC" <<'EOF'
source ~/.bashrc
eval "$(register-python-argcomplete yannt)"
EOF

exec bash --rcfile "$TMP_RC" -i
