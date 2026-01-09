#!/usr/bin/env bash

PROJ_PATH=$(realpath $(dirname $0)/..)

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

# TODO: These dependencies should be managed by pyproject.toml.
echo Checking dependencies.

pip show thirdparty_yannt &>/dev/null || pip install $PIP_ARGS -e yannt

# pip install for each extern
mkdir -p ${EXTERN_DIR}
for pkgpath in ${EXTERN_DIR}/*; do
  if [ -d "$pkgpath" ]; then
    pip show $(basename "$pkgpath") &>/dev/null || pip install -U $PIP_ARGS -e $pkgpath
  fi
done

echo
echo "The environment is now ready. Try 'yannt --help' for information."

# Include yannt tab completion.
TMP_RC="$(mktemp)"
cat >> "$TMP_RC" <<'EOF'
[ -f "~/.bashrc" ] && source ~/.bashrc
eval "$(register-python-argcomplete yannt)"
EOF

exec bash --rcfile "$TMP_RC" -i
