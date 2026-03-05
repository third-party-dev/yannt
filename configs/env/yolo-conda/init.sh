#!/usr/bin/env bash

set -e

# --------- Guard Against Uninitialized Environments -------

if [ -z "${PROJ_PATH}" ]; then
  echo "Please run via ./scripts/init-dev.sh."
  exit 1
fi

# The following should be set:
# PROJ_PATH - Full path to yannt
# CONFIG_NAME - Name of config folder
# CONFIG_PATH - Full path to config folder

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
source $(dirname $(dirname $(which conda)))/bin/activate

# Note: Assuming it is OK to not check if the environment exists.

# Create conda environment.
mkdir -p ${PROJ_PATH}/cache/conda/envs
conda create -y -c defaults -c conda-forge \
  -p ${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME} \
  python=3.11 ultralytics pytorch-cpu torchvision torchaudio onnx onnxslim onnxruntime

# Note: We lock the python version to something we know works with _most_ libraries
# and then install ultralytics with this constraint. The rest will hopefully fall
# in line. FYI, going with newness (python 3.14 circa 2026) does not have a lot of
# support across the ecosystem -yet.

# Activate environment
conda activate ${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME}

mkdir -p ${PROJ_PATH}/cache/pip_pkgs/3.11
# Note: ncnn or pnnx requires pytorch, causing the downloads to become CUDA based and large
pip download -d ${PROJ_PATH}/cache/pip_pkgs/3.11 \
  'paddlepaddle>=3.0.0,!=3.3.0' 'x2paddle' \
  ncnn pnnx \
  'coremltools>=9.0' \
  'openvino>=2024.0.0'

# Install python packages from cache.
pip install --no-index -f ${PROJ_PATH}/cache/pip_pkgs/3.11 \
  'paddlepaddle>=3.0.0,!=3.3.0' 'x2paddle' \
  ncnn pnnx \
  'coremltools>=9.0' \
  'openvino>=2024.0.0'

# -------------- Dropping to shell ----------------
if [ -z "$NO_SHELL" ]; then

echo
echo "The environment is now ready. Try 'yolo --help' for information."

# Include yannt tab completion.
TMP_RC="$(mktemp)"
cat >> "$TMP_RC" <<'EOF'
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc
export PATH=${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME}/bin:$PATH
source "$(dirname $(dirname $(which conda)))/bin/activate"
conda activate ${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME}
EOF

exec bash --rcfile "$TMP_RC" -i

fi