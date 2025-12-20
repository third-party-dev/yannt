#!/bin/sh

docker run -ti --rm -v $(pwd):/work -w /work python:3.13 pip download \
  torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cpu

docker run -ti --rm -v $(pwd):/work -w /work python:3.13 pip download \
  pip setuptools wheel build pytest transformers numpy protobuf
