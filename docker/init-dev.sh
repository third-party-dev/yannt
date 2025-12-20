#!/bin/sh

# Note: This script runs within docker container.
VENV_PATH=/work/ml-dev-venv

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
export ML_VENV_NAME=ml-dev-venv
/work/env.sh

# python3 -m venv $VENV_PATH \
#     && $VENV_PATH/bin/pip install --no-index --find-links /opt/pip_pkgs/ \
#         --upgrade pip setuptools wheel build pytest \
#     && chmod -R a+rX $VENV_PATH

# export PATH="$VENV_PATH/bin:$PATH"

# pip install --no-index --find-links /opt/pip_pkgs/ -e yannt

#     # Do each build in extern
#     mkdir -p "$LOCAL_DIR"
#     mkdir -p "$SRC_DIR"
#     rm -rf "$LOCAL_DIR"/*

#     for pkgpath in "$SRC_DIR"/*; do
#         if [ -d "$pkgpath" ]; then

#             # Skip if pkgname is in EXCLUDE_PKG list
#             pkgname=$(basename "$pkgpath")
#             skip=0
#             for e in $EXCLUDE_PKG; do
#                 [ "$pkgname" = "$e" ] && skip=1 && break
#             done
#             [ "$skip" -eq 1 ] && continue

#             echo "Building $pkgpath..."
#             (cd "$pkgpath" && python3 -m build >/dev/null 2>&1)

#             # Copy contents of dist/ to PIP_DIR
#             if [ -d "$pkgpath/dist" ]; then
#                 cp -r "$pkgpath"/dist/* "$LOCAL_DIR"/
#             fi
#         fi
#     done

#     # Special case for yannt
#     echo "Building yannt..."
#     (cd "yannt" && python3 -m build >/dev/null 2>&1)
#     cp -r "yannt/dist/"* "$LOCAL_DIR"/
# cd docker