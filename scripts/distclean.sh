#!/bin/sh

PROJ_PATH=$(realpath $(dirname $0)/..)

${PROJ_PATH}/scripts/clean.sh

rm -rf ${PROJ_PATH}/pip_pkgs
rm -rf ${PROJ_PATH}/.cache
