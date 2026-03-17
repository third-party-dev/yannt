#!/usr/bin/env bash

set -e

export PROJ_PATH=$(realpath $(dirname $0)/..)

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

# Build all the environments
for cfg in $(ls -1 ${PROJ_PATH}/configs/env); do
    echo "Initializing $cfg"
    NO_SHELL=1 ${PROJ_PATH}/scripts/init-dev.sh $cfg
done

# Activate each environment
source "$(dirname $(dirname $(which conda)))/bin/activate"
for cfg in $(ls -1 ${PROJ_PATH}/configs/env | grep -E '^py.*conda$'); do
    echo "Fetching pip freeze for $cfg"
    (   # Run the following config in its own shell.
        source ${PROJ_PATH}/configs/env/$cfg/config \
        && conda activate ${PROJ_PATH}/cache/conda/envs/${ML_VENV_NAME} \
        && pip freeze | grep -v ^-e > ${PROJ_PATH}/configs/env/$cfg/buildall-freeze.txt \
        && conda deactivate
    )
done


