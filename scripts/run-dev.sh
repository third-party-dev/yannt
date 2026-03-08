#!/usr/bin/env bash

#sudo apt install python3.13-venv
#sudo apt install python3-argcomplete
#sudo apt install python3-pip

set -e

export PROJ_PATH=${PROJ_PATH:-$(realpath $(dirname $0)/..)}
export CONFIG_NAME="$1"
export RUN_MODE="$2"
export CONFIG_PATH="${PROJ_PATH}/configs/env/${CONFIG_NAME}"

if [ -z "$CONFIG_NAME" -o "$CONFIG_NAME" = "list" ]; then
    ls -1 ${PROJ_PATH}/configs/env
    exit 0
fi

if [ ! -e "${CONFIG_PATH}" ]; then
    echo "Could not find config file for ${CONFIG_NAME}"
    exit 1
fi

${CONFIG_PATH}/run.sh $@
