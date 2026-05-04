#!/bin/sh

export PROJ_PATH=$(realpath $(dirname $0)/..)
cd ${PROJ_PATH}/docs/manual

# TODO: Do better dependency management. What things are creating
# TODO: what side effects?
# ! 4.2.3-pparse-pytorch-usecases.md fails if models/bert/pt exists.

echo "Preprocessing 4.1.1-hft-usecases.md"
./pandoc-build/inline_actions.py 4.1.1-hft-usecases.md

echo "Preprocessing 4.2.1-pparse-ident-usecases.md"
./pandoc-build/inline_actions.py 4.2.1-pparse-ident-usecases.md

echo "Preprocessing 4.2.2-pparse-safetensors-usecases.md"
./pandoc-build/inline_actions.py 4.2.2-pparse-safetensors-usecases.md

echo "Preprocessing 4.2.3-pparse-pytorch-usecases.md"
./pandoc-build/inline_actions.py 4.2.3-pparse-pytorch-usecases.md

echo "Preprocessing 4.2.6-pparse-pickle-usecases.md"
./pandoc-build/inline_actions.py 4.2.6-pparse-pickle-usecases.md

echo "Preprocessing 4.2.11-pparse-zip-usecases.md"
./pandoc-build/inline_actions.py 4.2.11-pparse-zip-usecases.md

echo "Preprocessing 4.2.12-pparse-json-usecases.md"
./pandoc-build/inline_actions.py 4.2.12-pparse-json-usecases.md

echo "Preprocessing 4.3.1-sysscan-usescases.md"
./pandoc-build/inline_actions.py 4.3.1-sysscan-usescases.md