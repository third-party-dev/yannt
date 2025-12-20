#!/bin/sh

set -e

HOST_PWD="$(realpath "$(pwd)")"
CONTAINER_PWD="/host${HOST_PWD}"

# Start container in project root.
# TODO: Get the realpath of folder above script path
PROJ_ROOT_PATH=$(realpath $(dirname $0)/..)

docker run -ti --rm \
  -v "$PROJ_ROOT_PATH":/work \
  -w /work \
  yannt-dev /bin/bash $@
