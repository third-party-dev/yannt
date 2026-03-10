#!/usr/bin/env bash

set -e

# Assuming we're in top level yannt folder.

EXTERN_DIR=./extern

# Allow user to assign venv name and tag shell prompt
ML_VENV_NAME=${ML_VENV_NAME:-ml-venv}

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

export PS1_TAG=${PS1_TAG:-"(${ML_VENV_NAME}) "}
export PS1="${PS1_TAG}${PS1:-\$ }"

# Assuming we've already collected.
PIP_INST_ARGS=${PIP_INST_ARGS:-"--no-index -f ./cache/pip_pkgs/${PY_VER}"}
PYTHON=${PYTHON:-python}
# # # echo "Running pip install of config packages."
# # # pip install -U ${PIP_INST_ARGS} ${PY_REQS_ARGS} ${PY_CONSTRAINTS_ARGS}

# # # # Note: These dependencies _should_ be managed by pyproject.toml.
# # # echo Checking dependencies.

# # # echo "Installing base yannt package in place (ie for development)."
# # # pip show thirdparty_yannt &>/dev/null || pip install -U ${PIP_INST_ARGS} -e yannt

# # # echo "Installing each package from ./extern in place (ie for development)."
# # # # pip install for each extern
# # # mkdir -p ${EXTERN_DIR}
# # # for pkgpath in ${EXTERN_DIR}/*; do
# # #   if [ -d "$pkgpath" ]; then
# # #     echo pip install -U ${PIP_INST_ARGS} -e $pkgpath ${PY_CONSTRAINTS_ARGS}
# # #     pip show $(basename "$pkgpath") &>/dev/null || pip install -U ${PIP_INST_ARGS} -e $pkgpath
# # #   fi
# # # done

mkdir -p ./cache/venv
if [ ! -e "./cache/venv/${ML_VENV_NAME}" ]; then
  # Note: The following line is the only place we enforce python version for venv.
  ${PYTHON} -m venv ./cache/venv/${ML_VENV_NAME}
  [ $? -ne 0 ] && { echo "Failed to create venv"; exit 1; }

  echo "--------------------- Setting Up Base Python Requirements ---------------------"
  ./cache/venv/${ML_VENV_NAME}/bin/pip install --upgrade \
    ${PIP_INST_ARGS} ${PY_REQS_ARGS} ${PY_CONSTRAINTS_ARGS}
fi
source ./cache/venv/${ML_VENV_NAME}/bin/activate
echo HERE4
# TODO: These dependencies should be managed by pyproject.toml.
echo Checking dependencies.

pip show thirdparty_yannt &>/dev/null || pip install ${PIP_INST_ARGS} \
  ${PY_CONSTRAINTS_ARGS} -e yannt

# pip install for each extern
mkdir -p ${EXTERN_DIR}
for pkgpath in ${EXTERN_DIR}/*; do
  if [ -d "$pkgpath" ]; then
    echo pip install -U ${PIP_INST_ARGS} -e $pkgpath ${PY_CONSTRAINTS_ARGS}
    pip show $(basename "$pkgpath") &>/dev/null || pip install -U ${PIP_INST_ARGS} \
      ${PY_CONSTRAINTS_ARGS} -e $pkgpath
  fi
done

if [ -z "$NO_SHELL" ]; then
  ./scripts/_/start-venv.sh $@
fi

# echo
# echo "The environment is now ready. Try 'yannt --help' for information."

# # Include yannt tab completion.
# TMP_RC="$(mktemp)"
# cat >> "$TMP_RC" <<'EOF'
# [ -f "~/.bashrc" ] && source ~/.bashrc
# source ${CRI_PROJ_PATH}/cache/venv/${ML_VENV_NAME}/bin/activate
# eval "$(register-python-argcomplete yannt)"
# EOF

# exec bash --rcfile "$TMP_RC" -i
