#!/usr/bin/env bash

PROJ_PATH=$(realpath $(dirname $0)/..)

# Run the jupyter environment
docker run -it --rm \
  -p 8888:8888 \
  -u $(id -u):$(id -g) \
  -v ${PROJ_PATH}:/home/jovyan/yannt \
  jupyter/base-notebook:python-3.9
