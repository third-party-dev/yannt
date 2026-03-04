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

if [ ! -e "${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME}" ]; then
  # If we're running an environment that doesn't exist, stop.
  echo "You are attempting to run an environment that doesn't exist. (${ML_VENV_NAME})"
  echo "Run: ./scripts/init-dev.sh ${CONFIG_NAME}"
  exit 1
fi

# Attempt to activate conda
if [ -z "$(which conda)" ]; then
  echo "Could not locate conda. Please add conda to PATH."
  echo "Example: export PATH=\$PATH:/opt/conda/bin"
  exit 1
fi
source $(dirname $(which conda))/activate

echo "Automatically accepting TOS."
conda tos accept

conda activate ${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME}

# -------------- Dropping to shell ----------------
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

