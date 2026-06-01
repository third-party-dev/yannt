#!/usr/bin/env bash

set -e

# Assuming we're in top level yannt folder.

EXTERN_DIR=./configs/auto_install

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
VENV_PYTHON=${VENV_PYTHON:-./cache/venv/${ML_VENV_NAME}/bin/python}

# Ensure virtualenv is available.
echo INSTALL VIRTUALENV: ${PYTHON} -m pip install --upgrade ${PIP_INST_ARGS} virtualenv
${PYTHON} -m pip install --upgrade ${PIP_INST_ARGS} virtualenv

mkdir -p ./cache/venv
if [ ! -e "./cache/venv/${ML_VENV_NAME}" ]; then
  # Note: The following line is the only place we enforce python version for venv.
  
  echo CREATE VENV: ${PYTHON} -m virtualenv ./cache/venv/${ML_VENV_NAME}
  ${PYTHON} -m virtualenv ./cache/venv/${ML_VENV_NAME}
  [ $? -ne 0 ] && { echo "Failed to create venv"; exit 1; }

  echo "--------------------- Setting Up Base Python Requirements ---------------------"
  ${VENV_PYTHON} -m pip install --upgrade \
    ${PIP_INST_ARGS} ${PY_REQS_ARGS} ${PY_CONSTRAINTS_ARGS}
fi
#source ./cache/venv/${ML_VENV_NAME}/bin/activate


# TODO: These dependencies should be managed by pyproject.toml.
echo Checking dependencies.

# pip install for each enabled
mkdir -p ${EXTERN_DIR}
for pkgpath in ${EXTERN_DIR}/*; do

  echo pkgpath = $pkgpath

  skip=0
  for blocked in $PKG_SKIP_LIST; do
    #echo blocked = ${EXTERN_DIR}/$blocked
    if [ "$pkgpath" = "${EXTERN_DIR}/$blocked" ]; then
      skip=1
      break
    fi
  done
  if [ "$skip" = "1" ]; then
    echo "Skipping $pkgpath."
    continue
  fi

  if [ -d "$pkgpath" ]; then
    echo ${VENV_PYTHON} -m pip show $(basename "$pkgpath") \&\>\/dev\/null 
    #bash -i
    ${VENV_PYTHON} -m pip show $(basename "$pkgpath")
    echo \|\| ${VENV_PYTHON} -m pip install -U ${PIP_INST_ARGS} ${PY_CONSTRAINTS_ARGS} -e $pkgpath
    ${VENV_PYTHON} -m pip show $(basename "$pkgpath") &>/dev/null \
    || ${VENV_PYTHON} -m pip install -U ${PIP_INST_ARGS} ${PY_CONSTRAINTS_ARGS} -e $pkgpath
  fi
done

echo STARTING CONTAINER

if [ -z "$NO_SHELL" ]; then
  ./scripts/_/start-venv.sh $@
fi


