#!/bin/sh

docker run -it --rm -p 8888:8888 \
  jupyter/base-notebook:python-3.9
