::: {.pagebreak-before}
:::

# Advanced Usage

This page mixes hand-written guidance with a block that a pre-processing
script rewrites in place before every build. Everything outside the
`GENERATED:` markers below is untouched by tooling and safe to edit by hand.

## Batch processing use case

When processing more than a few thousand widgets, prefer the batch API over
looping calls to `AcmeWidget.process()` one at a time -- see
[`AcmeWidget.process_batch`](../api/api-reference.md#acmewidget-process_batch)
for the full signature.

## Nightly benchmark results {#nightly-benchmark-results}

The table below is regenerated every night by `scripts/update_use_cases.py`
from the latest CI run. Do not hand-edit the region between the markers --
your changes will be overwritten on the next build.

<!-- GENERATED:BEGIN nightly-benchmarks -->
| Scenario | Throughput (widgets/s) | p99 latency |
| --- | --- | --- |
| cold start | 829 | 112 ms |
| warm cache | 5,104 | 8 ms |
| batch (1k) | 63,870 | 4 ms |

_Last refreshed: 2026-07-02T08:47:49Z from CI run `#4822`._
<!-- GENERATED:END nightly-benchmarks -->

## Interpreting the numbers

Warm-cache throughput assumes the widget registry has already been
populated by a prior call; see
[Install the CLI](getting-started.md#install-the-cli) if you haven't set one
up yet.
