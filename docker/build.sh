#!/bin/sh

PROJ_ROOT_PATH=$(realpath $(dirname $0)/..)
cd $PROJ_ROOT_PATH


# Define EXCLUDE_PKG as list of whitespace separated packages to exclude.
ARG1="$1"
SRC_DIR="./extern"
LOCAL_DIR="./docker/context/local_pkgs"


# Ensure there is a bin catch all folder
mkdir -p docker/context/bin


# pip download dependencies so we can build offline (ok to fail)
./docker/download.sh


if [ "$ARG1" = "dev" ]; then
    cd docker
    mkdir -p context/empty
    docker build -t yannt-dev -f Dockerfile.dev context/empty
    docker run -ti --rm \
        -v "$PROJ_ROOT_PATH":/work -w /work \
        -v "$PROJ_ROOT_PATH"/docker/context/pip_pkgs:/opt/pip_pkgs \
        yannt-dev /work/env.sh
    exit $?
fi


# Do each build in extern
mkdir -p "$LOCAL_DIR"
mkdir -p "$SRC_DIR"
rm -rf "$LOCAL_DIR"/*

for pkgpath in "$SRC_DIR"/*; do
    if [ -d "$pkgpath" ]; then

        # Skip if pkgname is in EXCLUDE_PKG list
        pkgname=$(basename "$pkgpath")
        skip=0
        for e in $EXCLUDE_PKG; do
            [ "$pkgname" = "$e" ] && skip=1 && break
        done
        [ "$skip" -eq 1 ] && continue

        echo "Building $pkgpath..."
        (cd "$pkgpath" && python3 -m build >/dev/null 2>&1)

        # Copy contents of dist/ to PIP_DIR
        if [ -d "$pkgpath/dist" ]; then
            cp -r "$pkgpath"/dist/* "$LOCAL_DIR"/
        fi
    fi
done


# Special case for yannt
echo "Building yannt..."
(cd "yannt" && python3 -m build >/dev/null 2>&1)
cp -r "yannt/dist/"* "$LOCAL_DIR"/


# Now run the Dockerfile build process.
cd docker
docker build -t yannt -f Dockerfile context
