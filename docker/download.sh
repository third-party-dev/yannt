#!/bin/sh

mkdir -p context/pip_pkgs

# Download CPU-only Torch separately
docker run -ti --rm -v $(pwd)/context/pip_pkgs:/work -w /work python:3.13-slim \
  pip download torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cpu

# Download all the other dependencies
docker run -ti --rm -v $(pwd)/context/pip_pkgs:/work -w /work python:3.13-slim \
  pip download pip setuptools wheel build pytest transformers numpy protobuf

# TODO: It would be preferred to dynamically determine this based on yannt and plugins.