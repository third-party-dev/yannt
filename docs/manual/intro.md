<!--
  crosslink_mode is intentionally NOT set here: it is supplied per-build on
  the pandoc command line (-M crosslink_mode=...) by scripts/build.sh, since
  it depends on which output we're producing, not on the content itself.

  Book-level metadata (title, author, date, ...) for the PDF/monolithic-HTML
  title page lives in docs/_meta/book.yaml, not here -- see that file for
  why it's kept separate from this page's own content.
-->


# Introduction

Welcome to the **Acme Widget SDK** manual. This document is authored as a
tree of Pandoc Markdown files under `docs/`, mirroring the folder layout a
Docusaurus `docs/` directory would use for its automatically-generated
sidebar.

This particular page is entirely hand-written. Other pages in this manual
mix hand-written prose with sections that are mechanically refreshed by a
pre-processing step (see [Use Cases](guides/advanced-usage.md#nightly-benchmark-results)),
and the [API Reference](api/api-reference.md#acmewidget) is generated
wholesale from source-level docstrings.

## What this manual covers

![Pipeline overview](assets/pipeline-diagram.svg)

- Getting the SDK installed and configured.
- Walking through the primary use cases.
- A full, cross-referenced API reference.

## A heading that stays out of the way {.unlisted}

Not everything needs a spot in the table of contents. This heading exists so
readers can still deep-link to this exact paragraph
(`#a-heading-that-stays-out-of-the-way`), but it won't show up as TOC noise
in the PDF or HTML outline. It still renders normally in the body text, and
still gets numbered like its siblings unless `.unnumbered` is added too.

See the [Getting Started guide](guides/getting-started.md#install-the-cli) to
begin.
