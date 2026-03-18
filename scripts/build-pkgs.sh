#!/usr/bin/env bash

export PROJ_PATH=$(realpath $(dirname $0)/..)
cd ${PROJ_PATH}

# Note: VERSION is git-ignored (not revision controlled)
if [ -z "$1" ]; then
  VERSION="0.0.0.dev0"
else
  VERSION=$1
fi

for pkg in packages/*; do
  if [ -e "packages/$pkg/.yannt-ignore" ]; then
    # package wants to be ignored by yannt processing
    continue
  fi
  echo "$VERSION" > "$pkg/VERSION"
done

# Rebuild all packages
mkdir -p outputs/dist
for pkg in packages/*; do
  (cd "$pkg" \
    && python -m build --outdir ${PROJ_PATH}/outputs/dist \
    && python -m build --sdist --outdir ${PROJ_PATH}/outputs/dist)
done

echo "!! Ensure clean repo before tagging. !!"
echo
echo git tag v$VERSION
echo
echo git push origin v$VERSION
echo