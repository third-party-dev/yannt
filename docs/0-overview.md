# Yet Another Neural Network Tool (yannt)

## Purpose

Yet Another Neural Network Tool (yannt) is a command line tool and suite of libraries for performing analysis and operations on machine learning models and environments. It is highly inspired by the work done by Netron, but in a way that is much less visual. The goal is to be able to parse model formats, convert model formats, and perform various analysis on model formats and the ML environment.

yannt itself is a command line interface wrapper and command line framework. In otherwords, none of the actual work mentioned above is performed by yannt. Instead you must install yannt plugins inside the same python (virtual) environment. The plugins themselves become subcommands of the top-level yannt command with their own arguments and handlers.

From strictly a user perspective, yannt is a single point of entry for discovering and using the plugins installed into the python environment. The most important of these plugins is the `pparse` plugin. The pparse plugin has its own documentation, but for now you should know that when installing `thirdparty.pparse` into a python environment, it enables:

- `import thirdparty.pparse.lib as pparse` - First and foremost, pparse is a python library that is designed to be imported and used by other python code. **Note: No testing in Jupyter Notebooks is performed. All testing is done with test scripts run from within the `env.sh` built virtual environment. Work is planned for supporting Jupyter Environments.**

- `yannt pparse [pparse-command] [options] [args]` - For CLI actions, its recommended to use yannt as the entrypoint. The CLI is primary intended for common task execution, data preparation, and user demonstration purposes. You get all of the power of the tools with your own python scripts, but sometimes you just want to copy paste some commands to get what you need.

- `pparse [pparse-command] [options] [args]` - For systems that are confident they only need pparse, you can install pparse by itself, without yannt. This was an easy addition based on how the argparse component was integrated so its nice to be able to quickly and independently test pparse commands.

## Getting started

I'm currently working on determining several different ways to manage working with the yannt framework. For now, I'll go through a developer central way to get things setup and going:

### Clone The Repos

To keep various capabilities independent and plugable, I've dividing things into their own repositories. Yannt is assumed to be at the top `./yannt` with all plugin source code cloned into yannt's extern folder `./yannt/extern/plugin-here`. The following commands should get you going (assuming bash-like shell):

```sh
# ! For _reasons_:
# ! - (atm) Assuming docker installed and current user has docker access.
# ! - (atm) Assuming systems has Python 3.13 (I'm using debian 13)
cd ~ ; mkdir thirdparty-ws ; cd thirdparty-ws
ln -s yannt/extern/pparse pparse
ln -s yannt/extern/pparse yannt-transformers
git clone https://github.com/third-party-dev/yannt.git
cd yannt ; mkdir extern ; cd extern
git clone https://github.com/third-party-dev/pparse.git thirdparty_pparse
git clone https://github.com/third-party-dev/yannt-transformers.git thirdparty_yannt_transformers
cd ..
# Setup virtual environment.
./env.sh
```

After you've run `./env.sh`, you'll be in a new shell that has been prefixed with `(ml-venv)` to indicate you are in the yannt python virtual environment. If everything when well, `yannt` tab completion should now also work. As per the usual `argparse` enabled command, you can also run `yannt --help` to get your barrings.

## Workspace Layout

- `thirdparty-ws` - The name of this folder can be anything, but I will normally name _workspace_ folders after the larger effort or epic that it is contributing too. Sometimes it becomes the forge organization.
- `thirdparty/yannt` - Top level git repo folder for yannt.
- `thirdparty-ws/pparse` - A symlink to the yannt extern/thirdparty_pparse. Avoids having multiple checkouts that could get out of sync.
- `thirdparty-ws/yannt_transformers` - A symlink to the yannt extern/thirdparty_yannt_transformers. Avoids having multiple checkouts that could get out of sync.

When working on the individual plugins, I treat them as their own independent projects and _then_ test them with `yannt` integration.

When performing any virtual environment updates or resets, I always perform them from the `thirdparty-ws/yannt` folder so I can make assumptions like: "all in-place installs will exist in `extern` relative to `yannt` top folder.". 

### `thirdpart-ws/yannt` Project Layout

- `bundles` - Only appears when `create-bundle.sh` is run. For reasons, I've used `git bundles` to copy repo around. **Git Ignored**
- `docker` - Docker related files.
- `docker/context` - Specific location for docker build context, but also location of thirdparty wheels and sdists. **Partialy Git Ignored**
- `docker/context/pip_pkgs` - Downloaded pip dependency location (from running `./download.sh` in docker folder). **Git Ignored**
- `docs` - Documentation folder with markdown content.
- `docs/pandoc-build` - Pandoc build source code for building the docs as a PDF. Symlinks to parent to access markdown.
- `extern` - In-place installs of (in development) yannt plugins. **Git Ignored**
- `ml-venv` - Python virtual environment (explicitly embeded into project folder). Note: Must be recreated if moved. **Git Ignored**
- `upstream` - Folder for holding upstream source code (e.g. pytorch source code). **Git Ignored**
- `yannt` - The top folder for the yannt python package distribution.
- `yannt/pyproject.toml` - Descriptor for the yannt python package distribution.
- `yannt/src` - `pyproject.toml` is defined to only read source from the yannt `src` folder for the package.
- `yannt/src/thirdparty/yannt/cli` - Actual code responsible for discovering registered plugins and integrating them into yannt subcommands.
- `yannt/src/thirdparty/yannt/plugins` - (unused) stub code for including _builtin_ plugins. In all cases thus far, I'd prefer to manage plugins as python package distributions that register yannt package entry points.

## Plugins

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
