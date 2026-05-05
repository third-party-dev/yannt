#!/bin/sh

export PROJ_PATH=$(realpath $(dirname $0)/..)
cd ${PROJ_PATH}/docs/manual

echo "Preprocessing 4.1.1-hft-usecases.md"
./pandoc-build/inline_actions.py 4.1.1-hft-usecases.md

echo "Preprocessing 4.2.1-pparse-ident-usecases.md"
./pandoc-build/inline_actions.py 4.2.1-pparse-ident-usecases.md

echo "Preprocessing 4.2.2-pparse-safetensors-usecases.md"
./pandoc-build/inline_actions.py 4.2.2-pparse-safetensors-usecases.md

echo "Preprocessing 4.2.3-pparse-pytorch-usecases.md"
./pandoc-build/inline_actions.py 4.2.3-pparse-pytorch-usecases.md

# protobuf
echo "Preprocessing 4.2.4-pparse-protobuf-usecases.md"
./pandoc-build/inline_actions.py 4.2.4-pparse-protobuf-usecases.md

###################### BROKEN ######################
# om
#echo "Preprocessing 4.2.5-pparse-om-usecases.md"
#./pandoc-build/inline_actions.py 4.2.5-pparse-om-usecases.md

echo "Preprocessing 4.2.6-pparse-pickle-usecases.md"
./pandoc-build/inline_actions.py 4.2.6-pparse-pickle-usecases.md

# onnx
echo "Preprocessing 4.2.7-pparse-onnx-usecases.md"
./pandoc-build/inline_actions.py 4.2.7-pparse-onnx-usecases.md

# mnn
echo "Preprocessing 4.2.8-pparse-mnn-usecases.md"
./pandoc-build/inline_actions.py 4.2.8-pparse-mnn-usecases.md

# flatbuffers
echo "Preprocessing 4.2.9-pparse-flatbuffer-usecases.md"
./pandoc-build/inline_actions.py 4.2.9-pparse-flatbuffer-usecases.md

# tflite
echo "Preprocessing 4.2.10-pparse-tflite-usecases.md"
./pandoc-build/inline_actions.py 4.2.10-pparse-tflite-usecases.md

echo "Preprocessing 4.2.11-pparse-zip-usecases.md"
./pandoc-build/inline_actions.py 4.2.11-pparse-zip-usecases.md

echo "Preprocessing 4.2.12-pparse-json-usecases.md"
./pandoc-build/inline_actions.py 4.2.12-pparse-json-usecases.md

echo "Preprocessing 4.3.1-sysscan-usescases.md"
./pandoc-build/inline_actions.py 4.3.1-sysscan-usescases.md