# API Reference

This chapter is generated in full by `scripts/gen_api_docs.py` from `docs/api/api-spec.json`. Do not hand-edit this file; edit the spec (or, in a real pipeline, the source docstrings) and regenerate.

## AcmeWidget {#acmewidget}

*(class)* `class AcmeWidget(config: WidgetConfig)`

AcmeWidget wraps a single configured connection to the widget registry. Instances are cheap to create but expensive to reconfigure, so most applications should construct one instance at startup and reuse it.

| Name | Kind | Summary |
| --- | --- | --- |
| [`process`](#acmewidget-process) | method | Process a single widget synchronously. |
| [`process_batch`](#acmewidget-process_batch) | method | Process many widgets concurrently. |
| [`region`](#acmewidget-region) | attribute | The AWS-style region this client is bound to. |

:::: {.member-rule}
::::

#### `process` {#acmewidget-process .unlisted .unnumbered}

`process(item: Widget) -> Result`

Runs the full validation and transformation pipeline on `item` and blocks until a result is available.

**Args:**

- `item` (`Widget`): The widget to process.

**Returns:** Result -- the processed output, or raises on validation failure.

**Raises:**

- `ValidationError`: if `item` fails schema validation.

:::: {.member-rule}
::::

#### `process_batch` {#acmewidget-process_batch .unlisted .unnumbered}

`process_batch(items: list[Widget], *, parallelism: int = 8) -> list[Result]`

Prefer this over calling `process` in a loop for more than a few hundred widgets; it batches network round-trips to the registry and processes up to `parallelism` items at once.

**Args:**

- `items` (`list[Widget]`): Widgets to process.
- `parallelism` (`int`): Maximum concurrent workers. Defaults to 8.

**Returns:** list[Result] -- results in the same order as `items`.

:::: {.member-rule}
::::

#### `region` {#acmewidget-region .unlisted .unnumbered}

`region: str`

Read-only after construction; create a new `AcmeWidget` to target a different region.

:::: {.namespace-rule}
::::

## WidgetConfig {#widgetconfig}

*(class)* `class WidgetConfig(name: str, region: str = "us-east")`

A plain value object. Construct once and share across as many AcmeWidget instances as needed.

| Name | Kind | Summary |
| --- | --- | --- |
| [`name`](#widgetconfig-name) | attribute | Human-readable workspace name. |
| [`region`](#widgetconfig-region) | attribute | Target region identifier. |

:::: {.member-rule}
::::

#### `name` {#widgetconfig-name .unlisted .unnumbered}

`name: str`

Shown in the Acme dashboard; has no functional effect.

:::: {.member-rule}
::::

#### `region` {#widgetconfig-region .unlisted .unnumbered}

`region: str`

Defaults to `"us-east"` when not supplied.
