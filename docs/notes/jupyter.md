# requirements

- Terminal virtual environment init (w/o Jupyter)

- Jupyter virtual environment init

- Install dependencies online `-f <url>`
- Install dependencies with `--no-index -f <url>`
  - Download dependencies



#!/bin/sh

docker run -it --rm -p 8888:8888 \
  jupyter/base-notebook:python-3.9



#!/usr/bin/env bash

PROJ_PATH=$(realpath $(dirname $0)/..)

# Run the jupyter environment
docker run -it --rm \
  -p 8888:8888 \
  -u $(id -u):$(id -g) \
  -v ${PROJ_PATH}:/home/jovyan/yannt \
  jupyter/base-notebook:python-3.9