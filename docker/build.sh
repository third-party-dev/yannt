#!/bin/sh

# Define EXCLUDE_PKG as list of whitespace separated packages to exclude.

SRC_DIR="./extern"
LOCAL_DIR="./docker/context/local_pkgs"

# Ensure there is a bin catch all folder
mkdir -p context/bin

# pip download dependencies so we can build offline (ok to fail)
./downlogfad.sh

cd ..
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
cd docker

# Now run the Dockerfile build process.
docker build -t yannt -f Dockerfile context
