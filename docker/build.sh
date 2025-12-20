#!/bin/sh

SRC_DIR="./extern"
DEST_DIR="./docker/context/pip_pkgs"

ARG1=$1



cd ..

    # Do each build in extern
    mkdir -p "$DEST_DIR"
    mkdir -p "$SRC_DIR"

    for pkgpath in "$SRC_DIR"/*; do
        if [ -d "$pkgpath" ]; then

            # Clean any previous build
            rm -rf "$pkgpath/dist"

            # Skip if pkgname is in EXCLUDE_PKG list
            pkgname=$(basename "$pkgpath")
            skip=0
            for e in $EXCLUDE_PKG; do
                [ "$pkgname" = "$e" ] && skip=1 && break
            done
            [ "$skip" -eq 1 ] && continue

            echo "Building $pkgpath..."
            (cd "$pkgpath" && python3 -m build)

            # Copy contents of dist/ to DEST_DIR
            if [ -d "$pkgpath/dist" ]; then
                cp -r "$pkgpath/dist/"* "$DEST_DIR/"
            fi
        fi
    done

    # Special case for yannt
    (cd "yannt" && python3 -m build)
    cp -r "yannt/dist/"* "$DEST_DIR/"

cd docker

mkdir -p context/bin

# Now run the Dockerfile build process.

if [ "$ARG1" = "offline" ]; then
    echo "Building with offline mode."
    docker build -t yannt \
      --build-arg PIP_INSTALL_FLAGS="--no-index --find-links /opt/pip_pkgs/" \
      --build-arg TORCH_FLAGS="" \
      -f Dockerfile context
    exit 1
fi

docker build -t yannt -f Dockerfile context

