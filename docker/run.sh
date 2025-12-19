#!/bin/sh

set -e

HOST_PWD="$(realpath "$(pwd)")"
CONTAINER_PWD="/host${HOST_PWD}"

docker run -ti --rm \
  -v /:/host \
  -w "$CONTAINER_PWD" \
  --entrypoint /bin/bash \
  yannt

#/opt/ml-venv/lib/python3.13/site-packages/torch/lib