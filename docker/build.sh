#!/bin/sh

SRC_DIR="./extern"
DEST_DIR="./docker/context"

cd ..

    # Do each build in extern
    mkdir -p "$DEST_DIR"
    mkdir -p "$SRC_DIR"
    for pkgpath in "$SRC_DIR"/*; do
        if [ -d "$pkgpath" ]; then
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
docker build -t yannt -f Dockerfile context
