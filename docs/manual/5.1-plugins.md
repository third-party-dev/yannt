# Plugin Conventions

By convention, the plugin will have a `yannt_plugin.py` somewhere in the package that resembles:

```python
def register_pparse(subparsers):
    pparse_parser = subparsers.add_parser("pparse", help="pparse command")
    # ... and so forth with argparse configuration ...
```

The `yannt_plugin.py` is then defined as a `"yannt_command"` entry point in the `pyproject.toml`:

```toml
[project.entry-points."yannt_command"]
# Register pparse as a yannt subcommand
pparse = "thirdparty.pparse.cli.yannt_plugin:register_pparse"
```

This convention allows for yannt to discover commands that were ment for it without having any prior knowledge of the plugin as pip install time of the plugin or yannt. This is what permits `pparse` to exist not just as a plugin, but also as an independent CLI and python library, regardless of yannt's existance.
