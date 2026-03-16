#!/usr/bin/env bash

set -e

export PROJ_PATH=${PROJ_PATH:-$(realpath $(dirname $0)/..)}
export PLUGIN=$1

cd ${PROJ_PATH}

if [ -z "$PLUGIN" ]; then
    echo "Must provide a plugin."
    echo "------------------------------------"
    ls -1 enabled
    exit 1
fi

if [ ! -e "./enabled/$PLUGIN" ]; then
    if [ ! -L "./enabled/$PLUGIN" ]; then
        echo "The plugin provided is not enabled."
        exit 1
    fi
fi

if [ ! -L "./enabled/$PLUGIN" ]; then
    echo "The plugin you provided is not a symlink. Therefore,"
    echo "you must manually remove it from enabled folder."
    exit 1
fi

rm enabled/$PLUGIN
