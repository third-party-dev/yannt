#!/bin/bash

export PROJ_PATH=${PROJ_PATH:-$(realpath $(dirname $0)/..)}
FPATH=${PROJ_PATH}/bundles/yannt-$(date +%Y%m%d).bundle

mkdir -p ${PROJ_PATH}/bundles
git bundle create ${FPATH} --all --since="30 days ago"
base64 ${FPATH} > ${FPATH}.base64.txt
echo "Created: ${FPATH}.base64.txt"
