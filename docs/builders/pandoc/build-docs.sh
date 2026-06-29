#!/usr/bin/env bash

# sudo apt-get update
# sudo apt install -y pandoc texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-plain-generic

# pandoc *.md --toc --number-sections --pdf-engine=xelatex -o book.pdf

set -e

export PROJ_PATH=$(realpath $(dirname $0)/../../..)
DOCS_PATH=$PROJ_PATH/docs/manual
TMPL_PATH=$PROJ_PATH/docs/builders/pandoc
OUT_PATH=$PROJ_PATH/outputs/docs/pandoc

CHAPTERS="
${DOCS_PATH}/0-contents/index.md
${DOCS_PATH}/1-introduction/index.md
${DOCS_PATH}/1-introduction/1.1-overview.md
${DOCS_PATH}/1-introduction/1.2-install.md
${DOCS_PATH}/2-end-user/index.md
${DOCS_PATH}/2-end-user/2.1-overview.md
${DOCS_PATH}/2-end-user/2.2-concepts.md
${DOCS_PATH}/2-end-user/2.3-troubleshooting.md
${DOCS_PATH}/3-integration/index.md
${DOCS_PATH}/3-integration/3.3-quick-start.md
${DOCS_PATH}/3-integration/3.4-concepts.md
${DOCS_PATH}/3-integration/3.5-gotchas.md
${DOCS_PATH}/3-integration/3.6-versioning.md
${DOCS_PATH}/4-use-cases/index.md
${DOCS_PATH}/4-use-cases/4.1-test-usecases.md
${DOCS_PATH}/4-use-cases/4.1.1-hft-usecases.md
${DOCS_PATH}/4-use-cases/4.1.2-yolo-usecases.md
${DOCS_PATH}/4-use-cases/4.2-pparse-usecases.md
${DOCS_PATH}/4-use-cases/4.2.1-pparse-ident-usecases.md
${DOCS_PATH}/4-use-cases/4.2.2-pparse-safetensors-usecases.md
${DOCS_PATH}/4-use-cases/4.2.3-pparse-pytorch-usecases.md
${DOCS_PATH}/4-use-cases/4.2.4-pparse-protobuf-usecases.md
${DOCS_PATH}/4-use-cases/4.2.5-pparse-om-usecases.md
${DOCS_PATH}/4-use-cases/4.2.6-pparse-pickle-usecases.md
${DOCS_PATH}/4-use-cases/4.2.7-pparse-onnx-usecases.md
${DOCS_PATH}/4-use-cases/4.2.8-pparse-mnn-usecases.md
${DOCS_PATH}/4-use-cases/4.2.9-pparse-flatbuffer-usecases.md
${DOCS_PATH}/4-use-cases/4.2.10-pparse-tflite-usecases.md
${DOCS_PATH}/4-use-cases/4.2.11-pparse-zip-usecases.md
${DOCS_PATH}/4-use-cases/4.2.12-pparse-json-usecases.md
${DOCS_PATH}/4-use-cases/4.3-analysis-usecases.md
${DOCS_PATH}/4-use-cases/4.3.1.1-analysis-factors-pparse-usecases.md
${DOCS_PATH}/4-use-cases/4.3.1.2-analysis-factors-tensorcharacter-usecases.md
${DOCS_PATH}/4-use-cases/4.4-misc-usecases.md
${DOCS_PATH}/4-use-cases/4.4.1-sysscan-usecases.md
${DOCS_PATH}/4-use-cases/4.4.x-python-usecases.md
${DOCS_PATH}/4-use-cases/4.5-naive-usecases.md
${DOCS_PATH}/4-use-cases/4.5.x-naive-mnn-usecases.md
${DOCS_PATH}/4-use-cases/4.5.x-naive-onnx-usecases.md
${DOCS_PATH}/4-use-cases/4.5.x-naive-pytorch-usecases.md
${DOCS_PATH}/4-use-cases/4.5.x-naive-safetensors-usecases.md
${DOCS_PATH}/4-use-cases/4.5.x-naive-tflite-usecases.md
${DOCS_PATH}/5-api-reference/index.md
${DOCS_PATH}/5-api-reference/5.2-test.md
${DOCS_PATH}/6-maintainer/index.md
${DOCS_PATH}/6-maintainer/6.2-architecture.md
${DOCS_PATH}/6-maintainer/6.3-dev-environment.md
${DOCS_PATH}/6-maintainer/6.4-code-base.md
${DOCS_PATH}/6-maintainer/6.5-testing/6.5.1-overview.md
${DOCS_PATH}/6-maintainer/6.6-release.md
${DOCS_PATH}/6-maintainer/6.7-roadmap.md
${DOCS_PATH}/6-maintainer/6.8-commentary/6.8.1-overview.md
${DOCS_PATH}/7-tutorials/index.md
${PROJ_PATH}/docs/builders/pandoc/api-doc-reference.md
"

# Excluded:
# - docs/5-api-reference/5.2-python-api.md

mkdir -p $OUT_PATH
cp $TMPL_PATH/api-doc.css $OUT_PATH/

echo "---- Building JSON"
pandoc $TMPL_PATH/metadata.yaml $CHAPTERS \
  --lua-filter=$TMPL_PATH/api-doc-filter.lua \
  --from markdown+raw_html+simple_tables \
  -o $OUT_PATH/api-doc-reference.json

echo "---- Building PDF"
pandoc $TMPL_PATH/metadata.yaml $CHAPTERS \
  --lua-filter=$TMPL_PATH/api-doc-filter.lua \
  --template=$TMPL_PATH/api-doc-template.latex \
  --pdf-engine=xelatex \
  --from markdown+raw_html+simple_tables \
  --toc \
  -o $OUT_PATH/api-doc-reference.pdf

echo "---- Building HTML"
pandoc $TMPL_PATH/metadata.yaml $CHAPTERS \
  --lua-filter=$TMPL_PATH/api-doc-filter.lua \
  --from markdown+raw_html+simple_tables \
  --toc \
  --standalone \
  --css=$TMPL_PATH/api-doc.css \
  -o $OUT_PATH/api-doc-reference.html

echo "---- Building EPUB"
pandoc $TMPL_PATH/metadata.yaml $CHAPTERS \
  --lua-filter=$TMPL_PATH/api-doc-filter.lua \
  --from markdown+raw_html+simple_tables \
  --toc \
  -o $OUT_PATH/api-doc-reference.epub















exit 0

# 

# cd $PROJ_PATH/docs/manual/pandoc-build



# --number-sections
# --listings

# NOTE: Ensure images have sufficiently high DPI. A standard 96 DPI image from a screenshot
#       will be oversized in the PDF. Try something like 300DPI or higher. FYI, most home
#       inkjet printers are 300-600 DPI, so this lines up. You can scale image DPI up and
#       down all day long and it will create zero pixel loss. Only the DPI header value
#       changes.

echo "Building JSON."
# pandoc metadata.yaml $CHAPTERS metadata-tail.yaml -t json > book.json
pandoc api-doc-reference.md \
  --lua-filter=api-doc-filter.lua \
  --from markdown+raw_html+simple_tables \
  -o api-doc-reference.json

echo "Building PDF."
# pandoc metadata.yaml $CHAPTERS metadata-tail.yaml \
#   --toc --pdf-engine=xelatex --template=template/eisvogel.tex \
#   --lua-filter=pandoc-filter.lua -o book.pdf #--verbose

pandoc api-doc-reference.md \
  --lua-filter=api-doc-filter.lua \
  --template=api-doc-template.latex \
  --pdf-engine=xelatex \
  --from markdown+raw_html+simple_tables \
  --toc \
  -V title="MyLibrary API Reference" \
  -V version="2.1.0" \
  -o api-doc-reference.pdf

echo "Building HTML"
pandoc api-doc-reference.md \
  --lua-filter=api-doc-filter.lua \
  --from markdown+raw_html+simple_tables \
  --toc \
  --standalone \
  -o api-doc-reference.html

echo "Building EPUB."
# pandoc metadata.yaml $CHAPTERS metadata-tail.yaml --toc -o book.epub

# pandoc api-doc-reference.md \
#   --lua-filter=api-doc-filter.lua \
#   --from markdown+raw_html+simple_tables \
#   --toc \
#   --epub-cover-image=cover.png \
#   -o api-doc-reference.epub

# pandoc api-doc-reference.md \
#   --lua-filter=api-doc-filter.lua \
#   --from markdown+raw_html+simple_tables \
#   --toc \
#   --css=api-doc.css \
#   -o api-doc-reference.epub