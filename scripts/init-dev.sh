#!/usr/bin/env bash

set -e

export PROJ_PATH=$(realpath $(dirname $0)/..)
export CONFIG_NAME="$1"
export CONFIG_PATH="${PROJ_PATH}/configs/env/${CONFIG_NAME}"

if [ -z "$CONFIG_NAME" -o "$CONFIG_NAME" = "list" ]; then
    ls -1 ${PROJ_PATH}/configs/env
    exit 0
fi

if [ ! -e "${CONFIG_PATH}/config" ]; then
    echo "Could not find config file for ${CONFIG_NAME}"
    exit 1
fi


${CONFIG_PATH}/init.sh $@


