# Getting Started

![Pipeline overview](../assets/pipeline-diagram.svg)

This page is hand-written and rarely changes.

## Install the CLI {#install-the-cli}

```bash
curl -fsSL https://get.acme.example/widget-cli | sh
widget-cli --version
```

## Configure your workspace

Create a `widget.toml` next to your project root:

```toml
[workspace]
name = "my-project"
region = "us-east"
```

Once configured, jump to [Advanced Usage](advanced-usage.md#nightly-benchmark-results)
for real numbers pulled from the latest nightly run, or straight to the
[`AcmeWidget` namespace](../api/api-reference.md#acmewidget) in the API
reference.
