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
  python=3.11 ultralytics pytorch-cpu torchvision torchaudio

conda activate ${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME}

# Cache the python packages.
mkdir -p ${PROJ_PATH}/cache/pip_pkgs/3.11
pip download -d ${PROJ_PATH}/cache/pip_pkgs/3.11 \
  'tensorflow>=2.0.0,<=2.19.0' 'tf_keras<=2.19.0' 'sng4onnx>=1.0.1' \
  'onnx_graphsurgeon>=0.3.26' 'ai-edge-litert>=1.2.0' 'onnx>=1.12.0,<2.0.0' \
  'onnx2tf>=1.26.3,<1.29.0' 'onnxslim>=0.1.71' 'onnxruntime' ultralytics-thop

# Install python packages from cache.
pip install --no-index -f ${PROJ_PATH}/cache/pip_pkgs/3.11 \
  'tensorflow>=2.0.0,<=2.19.0' 'tf_keras<=2.19.0' 'sng4onnx>=1.0.1' \
  'onnx_graphsurgeon>=0.3.26' 'ai-edge-litert>=1.2.0' 'onnx>=1.12.0,<2.0.0' \
  'onnx2tf>=1.26.3,<1.29.0' 'onnxslim>=0.1.71' 'onnxruntime' ultralytics-thop

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