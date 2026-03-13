#!/bin/bash

mkdir bundles
FPATH=./bundles/yannt_naive-$(date +%Y%m%d).bundle
git bundle create ${FPATH} --all
base64 ${FPATH} > ${FPATH}.base64.txt
echo "Created: ${FPATH}.base64.txt"
