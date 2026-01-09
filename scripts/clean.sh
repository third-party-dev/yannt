#!/bin/sh

PROJ_PATH=$(realpath $(dirname $0)/..)
cd ${PROJ_PATH}

# Dry run
#find . -type d \( -name "dist" -o -name "*.egg-info" \) -print

find . -type d \( -name "__pycache__" -o -name "*.egg-info" \) -prune -exec rm -rf {} +

rm -rf venv

# TODO: Do dist folders too.
