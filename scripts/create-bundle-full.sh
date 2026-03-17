#!/bin/bash

export PROJ_PATH=${PROJ_PATH:-$(realpath $(dirname $0)/..)}
FPATH=${PROJ_PATH}/cache/bundles/yannt-$(date +%Y%m%d)-full.bundle

mkdir -p ${PROJ_PATH}/cache/bundles
git bundle create ${FPATH} --all
base64 ${FPATH} > ${FPATH}.base64.txt
echo "Created: ${FPATH}.base64.txt"
