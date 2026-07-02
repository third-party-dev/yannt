#!/usr/bin/env bash

# sudo apt-get update
# sudo apt install -y pandoc texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-plain-generic

# pandoc *.md --toc --number-sections --pdf-engine=xelatex -o book.pdf

set -e

export PROJ_PATH=$(realpath $(dirname $0)/../../..)
DOCS_PATH=$PROJ_PATH/docs/manual
TMPL_PATH=$PROJ_PATH/docs/builders/pandoc
OUT_PATH=$PROJ_PATH/outputs/docs/pandoc
TARGET="${1:-all}"
TYPST=${TYPST:-typst}

CHAPTERS="
${DOCS_PATH}/0-contents/index.md
${DOCS_PATH}/1-introduction/index.md
${DOCS_PATH}/1-introduction/1.1-overview.md
${DOCS_PATH}/1-introduction/1.2-install.md
"
# ${DOCS_PATH}/2-end-user/index.md
# ${DOCS_PATH}/2-end-user/2.1-overview.md
# ${DOCS_PATH}/2-end-user/2.2-primers.md
# ${DOCS_PATH}/2-end-user/2.3-pparse-cli.md
# ${DOCS_PATH}/2-end-user/2.4-analysis-cli.md
# ${DOCS_PATH}/2-end-user/2.5-sysscan-cli.md
# ${DOCS_PATH}/2-end-user/2.x-troubleshooting.md
# ${DOCS_PATH}/3-integration/index.md
# ${DOCS_PATH}/3-integration/3.2-quick-start.md
# ${DOCS_PATH}/3-integration/3.3-yannt.md
# ${DOCS_PATH}/3-integration/3.4-analyze.md
# ${DOCS_PATH}/3-integration/3.5-pparse-view.md
# ${DOCS_PATH}/3-integration/3.6-pparse-lazy.md
# ${DOCS_PATH}/3-integration/3.7-pparse-lib.md
# ${DOCS_PATH}/3-integration/3.8-gotchas.md
# ${DOCS_PATH}/3-integration/3.9-versioning.md
# ${DOCS_PATH}/4-use-cases/index.md
# ${DOCS_PATH}/4-use-cases/4.1-test-usecases.md
# ${DOCS_PATH}/4-use-cases/4.1.1-hft-usecases.md
# ${DOCS_PATH}/4-use-cases/4.1.2-yolo-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2-pparse-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.1-pparse-ident-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.2-pparse-safetensors-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.3-pparse-pytorch-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.4-pparse-protobuf-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.5-pparse-om-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.6-pparse-pickle-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.7-pparse-onnx-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.8-pparse-mnn-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.9-pparse-flatbuffer-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.10-pparse-tflite-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.11-pparse-zip-usecases.md
# ${DOCS_PATH}/4-use-cases/4.2.12-pparse-json-usecases.md
# ${DOCS_PATH}/4-use-cases/4.3-analysis-usecases.md
# ${DOCS_PATH}/4-use-cases/4.3.1.1-analysis-factors-pparse-usecases.md
# ${DOCS_PATH}/4-use-cases/4.3.1.2-analysis-factors-tensorcharacter-usecases.md
# ${DOCS_PATH}/4-use-cases/4.4-misc-usecases.md
# ${DOCS_PATH}/4-use-cases/4.4.1-sysscan-usecases.md
# ${DOCS_PATH}/4-use-cases/4.4.x-python-usecases.md
# ${DOCS_PATH}/4-use-cases/4.5-naive-usecases.md
# ${DOCS_PATH}/4-use-cases/4.5.x-naive-mnn-usecases.md
# ${DOCS_PATH}/4-use-cases/4.5.x-naive-onnx-usecases.md
# ${DOCS_PATH}/4-use-cases/4.5.x-naive-pytorch-usecases.md
# ${DOCS_PATH}/4-use-cases/4.5.x-naive-safetensors-usecases.md
# ${DOCS_PATH}/4-use-cases/4.5.x-naive-tflite-usecases.md
# ${DOCS_PATH}/5-api-reference/index.md
# ${DOCS_PATH}/5-api-reference/5.2-test.md
# ${DOCS_PATH}/6-maintainer/index.md
# ${DOCS_PATH}/6-maintainer/6.2-architecture.md
# ${DOCS_PATH}/6-maintainer/6.3-dev-environment.md
# ${DOCS_PATH}/6-maintainer/6.4-code-base.md
# ${DOCS_PATH}/6-maintainer/6.5-testing/6.5.1-overview.md
# ${DOCS_PATH}/6-maintainer/6.6-release.md
# ${DOCS_PATH}/6-maintainer/6.7-roadmap.md
# ${DOCS_PATH}/6-maintainer/6.8-commentary/index.md
# ${DOCS_PATH}/6-maintainer/6.8-commentary/6.8.1-plugins.md
# ${DOCS_PATH}/6-maintainer/6.8-commentary/6.8.2-pparse.md
# ${DOCS_PATH}/6-maintainer/6.8-commentary/6.8.3-analysis.md
# ${DOCS_PATH}/6-maintainer/6.8-commentary/6.8.4-testing.md
# ${DOCS_PATH}/6-maintainer/6.8-commentary/6.8.5-naive.md
# ${DOCS_PATH}/6-maintainer/6.8-commentary/6.8.6-releasing.md
# ${DOCS_PATH}/7-tutorials/index.md
# ${PROJ_PATH}/docs/builders/pandoc/api-doc-reference.md
# "

RES_PATH_LIST="
${DOCS_PATH}/0-contents
${DOCS_PATH}/1-introduction
${DOCS_PATH}/2-end-user
${DOCS_PATH}/3-integration
${DOCS_PATH}/4-use-cases
${DOCS_PATH}/5-api-reference
${DOCS_PATH}/6-maintainer
${DOCS_PATH}/6-maintainer/6.5-testing
${DOCS_PATH}/6-maintainer/6.8-commentary
${DOCS_PATH}/6-maintainer/6.8-commentary/6.8.2-pparse
${DOCS_PATH}/6-maintainer/6.8-commentary/6.8.2-analysis
${DOCS_PATH}/7-tutorials
"

RES_PATHS=""
for item in $RES_PATH_LIST; do
    if [ -z "$RES_PATHS" ]; then
        RES_PATHS="$item"
    else
        RES_PATHS="$RES_PATHS:$item"
    fi
done

# Excluded:
# - docs/5-api-reference/5.2-python-api.md

# TODO: Consider putting side effect in create_folders procedure.
mkdir -p $OUT_PATH
cp $TMPL_PATH/manual.css $OUT_PATH/


FILTERS=( "$TMPL_PATH/toc-control.lua" "$TMPL_PATH/crosslink.lua" "$TMPL_PATH/rules.lua" )
filter_args() {
  local args=()
  for f in "${FILTERS[@]}"; do args+=(--lua-filter "$f"); done
  printf '%s\n' "${args[@]}"
}


build_json() {
  echo "---- Building JSON"
  pandoc $TMPL_PATH/metadata.yaml $CHAPTERS $TMPL_PATH/metadata-tail.yaml \
    $(filter_args) \
    -f markdown -t json \
    -o $OUT_PATH/api-doc-reference.json
}


build_typ() {
  echo "---- Building TYP"
  #local typ_out="$BUILD_DIR/manual.typ"
  #local pdf_out="$BUILD_DIR/manual.pdf"
  #local trace="$DEBUG_DIR/pdf-pandoc-trace.json"

  # shellcheck disable=SC2046
  trace="$OUT_PATH/yannt-manual-pandoc-typ-trace.json" \
  pandoc \
    $TMPL_PATH/metadata.yaml $CHAPTERS $TMPL_PATH/metadata-tail.yaml \
    -f markdown -t typst \
    --template "$TMPL_PATH/manual.typst" \
    --toc --toc-depth=3 \
    -M crosslink_mode=internal \
    $(filter_args) \
    --trace \
    -o "$OUT_PATH/yannt-manual.typ" \
    2>&1 | tee "$OUT_PATH/yannt-manual-pandoc-typ-stderr.log" 2>&1 >/dev/null
}


build_pdf() {
  echo "---- Building PDF"

  if command -v $TYPST >/dev/null 2>&1; then
    $TYPST compile "$OUT_PATH/yannt-manual.typ" "$OUT_PATH/yannt-manual.pdf" \
      2>&1 | tee "$OUT_PATH/pdf-typst-stderr.log"
  else
    echo "WARNING: 'typst' binary not found on PATH; skipping typst compile step."
    echo "  Install from https://github.com/typst/typst and re-run, or:"
    echo "    typst compile $OUT_PATH/yannt-manual.typ $OUT_PATH/yannt-manual.pdf"
  fi
}


build_single_html() {
  echo "---- Building Single HTML"
  cp $TMPL_PATH/manual.css $OUT_PATH/
  trace="$OUT_PATH/yannt-manual-pandoc-html-single-trace.json" \
  pandoc \
    $TMPL_PATH/metadata.yaml $CHAPTERS $TMPL_PATH/metadata-tail.yaml \
    -f markdown \
    -t html5 \
    -s --toc --toc-depth=3 \
    -M crosslink_mode=internal \
    --css=$OUT_PATH/manual.css \
    $(filter_args) \
    --trace \
    -o $OUT_PATH/yannt-manual-single.html \
    2>&1 | tee "$OUT_PATH/yannt-manual-pandoc-single-html-stderr.log" 2>&1 >/dev/null

}


build_multi_html() {
  echo "---- Building Multiple HTML"
  cp $TMPL_PATH/manual.css $OUT_PATH/
  local out_dir="$OUT_PATH/html"
  local stderr_log=$OUT_PATH/yannt-manual-pandoc-multi-html-stderr.log
  mkdir -p $out_dir

  echo "" > $stderr_log

  for src in $CHAPTERS; do
    local rel="${src#"${DOCS_PATH}"/}"
    local out="$out_dir/${rel%.md}.html"
    mkdir -p "$(dirname "$out")"
    pandoc "$src" \
      -f markdown \
      -t html5 \
      -s --toc --toc-depth=3 \
      -M crosslink_mode=html-multipage \
      --css=$OUT_PATH/manual.css \
      $(filter_args) \
      -o "$out" \
      2>&1 | tee -a "$stderr_log" 2>&1 >/dev/null
  done
}


build_commonmark() {
  echo "---- Building Multiple CommonMark"
  cp $TMPL_PATH/manual.css $OUT_PATH/
  local out_dir="$OUT_PATH/commonmark"
  local stderr_log=$OUT_PATH/yannt-manual-pandoc-multi-commonmark-stderr.log
  mkdir -p $out_dir

  echo "" > $stderr_log

  for src in $CHAPTERS; do
    local rel="${src#"${DOCS_PATH}"/}"
    local out="$out_dir/$rel"
    mkdir -p "$(dirname "$out")"

    pandoc "$src" \
      -f markdown \
      -t commonmark_x \
      --standalone \
      -M crosslink_mode=commonmark \
      $(filter_args) \
      -o "$out" \
      2>&1 | tee -a $stderr_log 2>&1 >/dev/null
  done
}


build_epub() {
  echo "---- Building EPUB"
  pandoc $TMPL_PATH/metadata.yaml $CHAPTERS $TMPL_PATH/metadata-tail.yaml \
    --lua-filter=$TMPL_PATH/api-doc-filter.lua \
    --from markdown+raw_html+simple_tables \
    --toc \
    -o $OUT_PATH/api-doc-reference.epub
}

case "$TARGET" in
  pdf)
    # preprocess
    build_json
    build_typ
    build_pdf
    ;;
  html)
    # preprocess
    build_single_html
    build_multi_html
    ;;
  commonmark)
    # preprocess
    build_commonmark
    ;;
  all)
    # preprocess
    build_json
    build_typ
    build_pdf
    build_single_html
    build_multi_html
    build_commonmark
    ;;
  *)
    echo "usage: $0 [pdf|html|commonmark|all]" >&2
    exit 2
    ;;
esac














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