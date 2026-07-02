#!/usr/bin/env bash
# scripts/build.sh
#
# Orchestrates the whole documentation pipeline:
#
#   1. Run pre-processors (regenerate dynamic sections + the API reference).
#   2. Build the PDF: every source file concatenated into ONE pandoc pass
#      (so Pandoc computes a single TOC/outline across the whole manual),
#      compiled Markdown -> Typst -> PDF.
#   3. Build HTML: both a single monolithic page AND a multi-page tree,
#      since the pipeline needs to support either.
#   4. Build CommonMark: each source file individually, cross-file links
#      left untouched, ready to drop into a Docusaurus `docs/` tree.
#   5. Dump JSON/debug artifacts for every step for troubleshooting.
#
# Usage: scripts/build.sh [pdf|html|commonmark|all]  (default: all)

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="$ROOT_DIR/docs"
BUILD_DIR="$ROOT_DIR/build"
DEBUG_DIR="$BUILD_DIR/debug"
FILTERS=( "$ROOT_DIR/filters/toc-control.lua" "$ROOT_DIR/filters/crosslink.lua" "$ROOT_DIR/filters/rules.lua" )
TEMPLATE="$ROOT_DIR/template/manual.typst"

TARGET="${1:-all}"

mkdir -p "$BUILD_DIR" "$DEBUG_DIR" "$BUILD_DIR/html-multipage" "$BUILD_DIR/commonmark"

log() { printf '\033[1;34m==>\033[0m %s\n' "$*"; }

filter_args() {
  local args=()
  for f in "${FILTERS[@]}"; do args+=(--lua-filter "$f"); done
  printf '%s\n' "${args[@]}"
}

# Manual page order. This is the single source of truth for reading order in
# the monolithic PDF / single-page HTML; the same files are discovered by
# folder for the per-file CommonMark/multi-page-HTML builds.
MANUAL_FILES=(
  "$DOCS_DIR/intro.md"
  "$DOCS_DIR/guides/getting-started.md"
  "$DOCS_DIR/guides/advanced-usage.md"
  "$DOCS_DIR/api/api-reference.md"
)

step_preprocess() {
  log "Pre-processing: refreshing generated sections"
  python3 "$ROOT_DIR/scripts/update_use_cases.py" \
    "$DOCS_DIR/guides/advanced-usage.md" \
    --debug-json "$DEBUG_DIR/use-case-refresh.json"

  log "Pre-processing: regenerating API reference"
  python3 "$ROOT_DIR/scripts/gen_api_docs.py" \
    "$DOCS_DIR/api/api-spec.json" \
    "$DOCS_DIR/api/api-reference.md" \
    --debug-json "$DEBUG_DIR/api-gen-report.json"
}

step_pdf() {
  log "Building PDF (single pandoc pass -> Typst -> PDF)"
  local typ_out="$BUILD_DIR/manual.typ"
  local pdf_out="$BUILD_DIR/manual.pdf"
  local trace="$DEBUG_DIR/pdf-pandoc-trace.json"

  # shellcheck disable=SC2046
  pandoc \
    "${MANUAL_FILES[@]}" \
    -f markdown \
    -t typst \
    --template "$TEMPLATE" \
    --toc --toc-depth=3 \
    -M crosslink_mode=internal \
    $(filter_args) \
    --trace \
    -o "$typ_out" \
    2> "$DEBUG_DIR/pdf-pandoc-stderr.log"

  log "Wrote intermediate Typst source: $typ_out"

  if command -v typst >/dev/null 2>&1; then
    typst compile "$typ_out" "$pdf_out" 2> "$DEBUG_DIR/pdf-typst-stderr.log" \
      && log "Wrote PDF: $pdf_out" \
      || { log "typst compile failed; see $DEBUG_DIR/pdf-typst-stderr.log"; return 1; }
  else
    log "WARNING: 'typst' binary not found on PATH; skipping typst compile step."
    log "  Install from https://github.com/typst/typst and re-run, or:"
    log "    typst compile '$typ_out' '$pdf_out'"
  fi
}

step_html_monolithic() {
  log "Building monolithic HTML (single pandoc pass, one page)"
  local out="$BUILD_DIR/manual.html"
  # shellcheck disable=SC2046
  pandoc \
    "${MANUAL_FILES[@]}" \
    -f markdown \
    -t html5 \
    -s --toc --toc-depth=3 \
    -M crosslink_mode=internal \
    --css=../assets/manual.css \
    $(filter_args) \
    -o "$out" \
    2> "$DEBUG_DIR/html-monolithic-stderr.log"
  log "Wrote: $out"
}

step_html_multipage() {
  log "Building multi-page HTML (one pandoc pass per source file)"
  local out_dir="$BUILD_DIR/html-multipage"
  for src in "${MANUAL_FILES[@]}"; do
    local rel="${src#"$DOCS_DIR"/}"
    local out="$out_dir/${rel%.md}.html"
    mkdir -p "$(dirname "$out")"
    # shellcheck disable=SC2046
    pandoc "$src" \
      -f markdown \
      -t html5 \
      -s --toc --toc-depth=3 \
      -M crosslink_mode=html-multipage \
      --css=../../assets/manual.css \
      $(filter_args) \
      -o "$out" \
      2>> "$DEBUG_DIR/html-multipage-stderr.log"
    log "Wrote: $out"
  done
}

step_commonmark() {
  log "Building CommonMark tree for Docusaurus (one pandoc pass per file)"
  local out_dir="$BUILD_DIR/commonmark"
  for src in "${MANUAL_FILES[@]}"; do
    local rel="${src#"$DOCS_DIR"/}"
    local out="$out_dir/$rel"
    mkdir -p "$(dirname "$out")"
    # shellcheck disable=SC2046
    pandoc "$src" \
      -f markdown \
      -t commonmark_x \
      --standalone \
      -M crosslink_mode=commonmark \
      $(filter_args) \
      -o "$out" \
      2>> "$DEBUG_DIR/commonmark-stderr.log"
    log "Wrote: $out"
  done
}

step_debug_summary() {
  log "Writing combined debug/troubleshooting report"
  python3 - "$DEBUG_DIR" <<'PYEOF'
import json, sys, pathlib, subprocess, datetime

def main():
  debug_dir = pathlib.Path(sys.argv[1])
  report = {
      "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "pandoc_version": subprocess.run(["pandoc", "--version"], capture_output=True, text=True).stdout.splitlines()[0],
      "typst_version": None,
      "artifacts": {},
  }
  try:
      r = subprocess.run(["typst", "--version"], capture_output=True, text=True)
      report["typst_version"] = r.stdout.strip() or r.stderr.strip()
  except FileNotFoundError:
      report["typst_version"] = "NOT INSTALLED"

  for f in sorted(debug_dir.glob("*")):
      if f.name == "build-summary.json":
          continue
      report["artifacts"][f.name] = {
          "size_bytes": f.stat().st_size,
          "path": str(f),
      }

  out = debug_dir / "build-summary.json"
  out.write_text(json.dumps(report, indent=2))
  print(f"wrote: {out}")
main()
PYEOF
}

case "$TARGET" in
  pdf)
    step_preprocess
    step_pdf
    ;;
  html)
    step_preprocess
    step_html_monolithic
    step_html_multipage
    ;;
  commonmark)
    step_preprocess
    step_commonmark
    ;;
  all)
    step_preprocess
    step_pdf
    step_html_monolithic
    step_html_multipage
    step_commonmark
    ;;
  *)
    echo "usage: $0 [pdf|html|commonmark|all]" >&2
    exit 2
    ;;
esac

step_debug_summary
log "Done. See $DEBUG_DIR for troubleshooting artifacts."
