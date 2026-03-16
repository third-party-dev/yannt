#!/usr/bin/env bash

# The following should be set:
# PROJ_PATH - Full path to yannt
# CONFIG_NAME - Name of config folder
# CONFIG_PATH - Full path to config folder

set -e

# --------- Guard Against Uninitialized Environments -------

if [ -z "${PROJ_PATH}" ]; then
  echo "Please run via ./scripts/init-dev.sh."
  exit 1
fi

# -------- Initialize CONDA Environment ---------

# Load environment configuration
source ${CONFIG_PATH}/config

# Attempt to activate conda
if [ -z "$(which conda)" ]; then
  echo "Could not locate conda. Please add conda to PATH."
  echo 
  echo "  Example: export PATH=\$PATH:/opt/conda/bin"
  echo
  echo "To install from upstream (~150M download and assuming write perms to /opt):"
  echo
  echo "  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
  echo "  chmod +x Miniconda3-latest-Linux-x86_64.sh"
  echo "  ./Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3"
  exit 1
fi
source $(dirname $(which conda))/activate

# Note: Assuming it is OK to not check if the environment exists.

#echo "Automatically accepting TOS."
#conda tos accept

# Create conda environment.
mkdir -p ${PROJ_PATH}/cache/conda/envs
conda create -y -c defaults -c conda-forge \
  -p ${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME} \
  python=${PY_VER}

conda activate ${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME}

# ---------- Initialize python environment -----------

# Note: We do this directly with conda in contrast to venv

# There are some assumptions that current folder is ${PROJ_PATH}
cd ${PROJ_PATH}
EXTERN_DIR=./enabled

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

# ----------- Fetch And Cache Dependencies -------------

if [ -z "$SKIP_COLLECT" ]; then

  PIP_DL_ARGS=${PIP_DL_ARGS:-"${PIP_IDX_ARGS} -d ${PROJ_PATH}/cache/pip_pkgs/${PY_VER}"}
  mkdir -p ${PROJ_PATH}/cache/pip_pkgs/${PY_VER}

  # Note: Only works when we assume python is version $PY_VER
  pip download ${PIP_DL_ARGS} ${PY_REQS_ARGS} ${PY_CONSTRAINTS_ARGS}

  # # Do given python packages
  # for arg in "$@"; do
  #     
  # done
  # Do for yannt
  pip download ${PIP_DL_ARGS} ${PY_CONSTRAINTS_ARGS} ${PROJ_PATH}/yannt

  # Do enabled python packages
  for ext in `ls -1 ${EXTERN_DIR}`; do
      pip download ${PIP_DL_ARGS} ${PY_CONSTRAINTS_ARGS} ${EXTERN_DIR}/$ext
  done

fi

# ----------- Install python dependencies -------------

PIP_INST_ARGS=${PIP_INST_ARGS:-"--no-index -f ${PROJ_PATH}/cache/pip_pkgs/${PY_VER}"}

echo "Running pip install of config packages."
pip install -U ${PIP_INST_ARGS} ${PY_REQS_ARGS} ${PY_CONSTRAINTS_ARGS}

# Note: These dependencies _should_ be managed by pyproject.toml.
echo Checking dependencies.

echo "Installing base yannt package in place (ie for development)."
pip show thirdparty_yannt &>/dev/null || pip install -U ${PIP_INST_ARGS} -e yannt

echo "Installing each package from ./enabled in place (ie for development)."
# pip install for each enabled
mkdir -p ${EXTERN_DIR}
for pkgpath in ${EXTERN_DIR}/*; do
  if [ -d "$pkgpath" ]; then
    echo pip install -U ${PIP_INST_ARGS} -e $pkgpath ${PY_CONSTRAINTS_ARGS}
    pip show $(basename "$pkgpath") &>/dev/null || pip install -U ${PIP_INST_ARGS} -e $pkgpath
  fi
done

# -------------- Dropping to shell ----------------
if [ -z "$NO_SHELL" ]; then

echo
echo "The environment is now ready. Try 'yannt --help' for information."

# Include yannt tab completion.
TMP_RC="$(mktemp)"
cat >> "$TMP_RC" <<'EOF'
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc
export PATH=${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME}/bin:$PATH
eval "$(register-python-argcomplete yannt)"
source "$(dirname $(dirname $(which conda)))/bin/activate"
conda activate ${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME}
EOF

exec bash --rcfile "$TMP_RC" -i

fi