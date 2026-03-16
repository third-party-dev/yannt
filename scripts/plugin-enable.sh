#!/usr/bin/env bash

set -e

export PROJ_PATH=${PROJ_PATH:-$(realpath $(dirname $0)/..)}
export PLUGIN=$1

cd ${PROJ_PATH}

if [ -z "$PLUGIN" ]; then
    echo "Must provide a plugin."
    echo "------------------------------------"
    ls -1 plugins
fi

mkdir -p ./enabled
ln -s ../plugins/$PLUGIN ./enabled/$PLUGIN