#!/usr/bin/env bash

set -e

export PROJ_PATH=${PROJ_PATH:-$(realpath $(dirname $0)/..)}
export SUBCMD=$1
export PACKAGE=$2

cd ${PROJ_PATH}
AUTOPATH=configs/auto_install
mkdir -p ${AUTOPATH}

if [ "$SUBCMD" = "enable" ]; then

    if [ -z "$PACKAGE" ]; then
        echo "Must provide a package to enable."
        echo "------------------------------------"
        ls -1 packages
        exit 0
    fi
    
    # Check if the target path is already used.
    if [ -e "${AUTOPATH}/$PACKAGE" -o -L "${AUTOPATH}/$PACKAGE" ]; then
        echo "$pkg already exists in ${AUTOPATH}. Skipping."
        exit 0
    fi

    # If a package folder name exists, it takes precedence.
    if [ -d "packages/$PACKAGE" ]; then
        RELPATH=$(realpath --relative-to="${AUTOPATH}" "packages/$PACKAGE")
        ln -s "$RELPATH" ${AUTOPATH}/$(basename "$PACKAGE")
        exit 0
    fi

    # Is the plugin a valid path? Use the basename as package folder.
    if [ -d "$PACKAGE" ]; then
        RELPATH=$(realpath --relative-to="${AUTOPATH}" "$PACKAGE")
        ln -s "$RELPATH" ${AUTOPATH}/$(basename "$PACKAGE")
        exit 0
    fi

    echo "Could not find package folder given: $PACKAGE"
    exit 1

elif [ "$SUBCMD" = "disable" ]; then

    if [ -z "$PACKAGE" ]; then
        echo "Must provide an _enabled_ package to disable."
        echo "------------------------------------"
        ls -1 ${AUTOPATH}
    fi

    if [ ! -e "${AUTOPATH}/$PACKAGE" ]; then
        if [ ! -L "./configs/auto_install/$PACKAGEN" ]; then
            # Here, the package is invalid path and not a symlink.
            echo "The plugin provided is not enabled."
            exit 1
        fi
    fi

    if [ ! -L "${AUTOPATH}/$PACKAGE" ]; then
        echo "The plugin you provided is not a symlink. Therefore,"
        echo "you must manually remove it from enabled folder."
        exit 1
    fi

    rm "${AUTOPATH}/$PACKAGE"


elif [ "$SUBCMD" = "enable-all" ]; then
    for pkg in $(ls -1 packages); do
        ./scripts/auto-package.sh enable $pkg
    done
elif [ "$SUBCMD" = "disable-all" ]; then
    for pkg in $(ls -1 ${AUTOPATH}); do
        ./scripts/auto-package.sh disable $pkg
    done
else
    echo "Please use a valid sub command:"
    echo
    echo "  $0 enable <package-folder>"
    echo "  $0 disable <package-folder>"
    echo "  $0 enable-all"
    echo "  $0 disable-all"
    echo
fi

