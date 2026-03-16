# Getting Started

Note: **WIP**

When getting started with yannt, you need to know if you plan to interact with the code as a developer/builder or a user. If you are going to be in the developer/builder camp, you'll want to start with the "Developer Environment Setup" instructions.

<!-- ## Jupyter

I'm currently unsure of the user workflows within Jupyter, therefore I've constructed a minimal viable thing to test code in Jupyter. Roughly, you must start a Jupyter docker image with the `yannt` project mounted. Connect to the Jupyter instance and manually install yannt as if it was on a local host. The following example shows the scripts to run to install with pip.

Build yannt Project for version in Jupyter: `PY_VER=3.9 ./scripts/build-docker-local-prod.sh`

Start the Jupyter docker container: ./scripts/start-docker-local-jupyter.sh

Inspect the Jupyter logs to get the token to access the localhost instance. Once connected, open a terminal and change directory (`cd`) into yannt folder. Then install with pip by running: `SKIP_COLLECT=1 ./scripts/install-host-local-pip.sh`.

Optionally, enable tab completion in the temrinal with: `source ./scripts/bash-tab-complete.sh`.

## Pipx

Before using `pipx`, please ensure its installed and within your path:

- Install pipx on Debian: `sudo apt update && sudo apt install pipx python3-pip`
- Install pipx on other systems: `python3 -m pip install --user pipx`

Since there is currently no upstream yannt, you must first build the yannt packages and then install via pipx from a local folder. You can choose to install with localized (offline) dependencies or upstream dependencies.

Build yannt Project: `./scripts/build-docker-local-prod.sh`

Offline yannt pipx Install: `SKIP_COLLECT=1 ./scripts/install-host-local-pipx.sh`

Online yannt pipx install: `./scripts/install-host-upstream-pipx.sh`

Now you should have `yannt` as a command in your normal (user) system environment. -->

## Developer Environment Setup

To keep various yannt components independent and plug-able, many components are divided up into their own repositories. Yannt manages the top level project folder for itself and all of its plugins. By convention, I always `git clone` yannt into a folder named `yannt`. All plugins (i.e. not builtin plugins) are `git cloned` into `yannt/enabled` with a python safe version of the package name. For example, `thirdpary.pparse` becomes `yannt/enabled/thirdparty_pparse` and `thirdparty.yannt.sysscan` becomes `yannt/enabled/thirdparty_yannt_sysscan`.

Commands similar to the following should get you going (assuming bash-like shell):

```sh
# Note: thirdparty-ws folder optional. Its a nice folder to open an IDE (e.g. VSCode) with.
cd ~ ; mkdir thirdparty-ws ; cd thirdparty-ws
ln -s yannt/enabled/thirdparty_pparse pparse
ln -s yannt/enabled/thirdparty_yannt_transformers yannt_transformers
git clone https://github.com/third-party-dev/yannt.git yannt
cd yannt ; mkdir enabled ; cd enabled
git clone https://github.com/third-party-dev/pparse.git thirdparty_pparse
git clone https://github.com/third-party-dev/yannt_sysscan.git thirdparty_yannt_sysscan
# ... git clone any additional plugins that you want to work with, using this convention ...
# go back to top yannt folder (not thirdparty-ws)
cd ..
```

Once you have the environment cloned locally into the workspace (`thirdparty-ws`) or project (`yannt`) folders, you'll want to initialize the environment for developer activities. See the following sections for the options.

### Initializing The Environment

Note: As a proposed simplification for running various build, install, or run command, I've added a Justfile and an adhoc implementation of the `just` command to the project as the `do` script. If you have the `just` command, that will work in place of `do`. I will use `do` for the rest of the documentation.

Environment initialization is managed by a collection of configurations stored in the `config` folder. You can see the available configurations via `./do init` (without parameters). For example:

```text
yannt-py3.11-conda
yannt-py3.11-docker
yannt-py3.11-podman
...
```

Each of the above strings is a procedure and reference to a development environment that you can build locally on your system. The configurations that start with `yannt` target environments that run the `yannt` command. The `py` part specifies the Python interpreter version that will be used, and the last part of the tuple is the type of environment that will manage the isolation. At the moment, yannt supports conda (for data science setups), docker for stronger isolation w/ GPU based setups, and podman for when conda is not available or discouraged in data science setups.

Note: Yannt intends to be available as a wheel that can be installed in any environment within a range of python interpreters. But this is the development environment initialization and therefore is limited to what will be supported and tested.

Once you've identified a configuration to run with (e.g. `yannt-py3.11-podman`), you can run:

```sh
./do init yannt-py3.11-podman
```

The scripts will attempt to set up a new environment with Python 3.11 and all of the required Python dependencies. As part of the process, the yannt development environment will attempt to download all of the dependencies into a cache folder before performing any installs. This extra cache process is independent of pip caching and ensures that all of the python packages are available for offline usage, keeps the packages more fixed, and allows developers positive control of the packages that are being installed, regardless of the `pyproject.yaml` or requirements/constraints settings. Plus you get a built-in local repository to prevent having to redownload CUDA packages for each re-initialization of the same python version.

Once the environment has been initialized, it will drop the user into a shell within the environment. If all went well you'll see something like the following:

```text
The environment is now ready. Try 'yannt --help' for information.
(yannt-py3.11-podman) user@61cc16f975c6:/work$
```

When you are done using the development environment or want to exit the environment, simply run `exit` (i.e. do not `deactivate` when that would seem appropriate, just `exit`). By design, the development environment is always initialized in a sub-shell of the one that `./do` was executed from. **This pattern prevents the development environment from polluting the original environment.**

### Running Already Created Environment

Similar to initialization, there is a process for running an already created (or initialized) environment. If you created `yannt-py3.11-podman`, you can use the pre-cached environment by running:

```sh
./do run yannt-py3.11-podman
```

Optionally, you don't need to run everything from a shell in the container. You can often accomplish single runs by providing `--` and the command you want to run. For example:

```sh
./do run yannt-py3.11-podman -- yannt --help
```

### Bash Tab Completion

As part of the developer environment, bash tab completion is included for `yannt` command. As per the usual `argparse` enabled command, you can also run `yannt --help` to get your barrings.
