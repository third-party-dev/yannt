#!/bin/sh

export PROJ_PATH=$(realpath $(dirname $0)/..)
cd ${PROJ_PATH}/docs/manual

./pandoc-build/inline_actions.py 1-overview.md

# rm -rf ${PROJ_PATH}/outputs/manual-build
# mkdir -p ${PROJ_PATH}/outputs/manual-build

# cp -r ${PROJ_PATH}/docs/manual ${PROJ_PATH}/outputs/manual-build


