# Getting Started

** WIP **

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

To keep various yannt components independent and plug-able, many components are divided up into their own repositories. Yannt manages the top level project folder for itself and all of its plugins. By convention, I always `git clone` yannt into a folder named `yannt`. All external plugins (i.e. not builtin plugins) are `git cloned` into `yannt/extern` with a python safe version of the package name. For example, `thirdpary.pparse` becomes `yannt/extern/thirdparty_pparse` and `thirdparty.yannt.sysscan` becomes `yannt/extern/thirdparty_yannt_sysscan`.

Commands similar to the following should get you going (assuming bash-like shell):

```sh
# Note: thirdparty-ws folder optional. Its a nice folder to open an IDE (e.g. VSCode) with.
cd ~ ; mkdir thirdparty-ws ; cd thirdparty-ws
ln -s yannt/extern/thirdparty_pparse pparse
ln -s yannt/extern/thirdparty_yannt_transformers yannt_transformers
git clone https://github.com/third-party-dev/yannt.git yannt
cd yannt ; mkdir extern ; cd extern
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

Each of the above strings is a procedure and reference to a development environment that you can build locally on your system. The configurations that start with `yannt` target environments that run the `yannt` command. The `py` part specifies the Python interpreter that will be used, and the last part of the tuple is the type of environment that will manage the isolation. At the moment, yannt supports conda (for data science setups), docker for stronger isolation w/ GPU based setups, and podman for when conda is not available or discouraged in data science setups.

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

When you are done using the development environment or want to exit the environment, simply run `exit` (i.e. do not `deactivate` when that would seem appropriate, just `exit`). By design, the development environment is always initialized in a sub-shell of the one that `./do` was executed from. This pattern prevents the development environment from polluting the original environment.

### Running Already Created Environment

Similar to initialization, there is a process for running an already created environment. If you created `yannt-py3.11-podman`, you can use the pre-cached environment by running:

```sh
./do run yannt-py3.11-podman
```

### Bash Tab Completion

As part of the developer environment, bash tab completion is included for `yannt` command. As per the usual `argparse` enabled command, you can also run `yannt --help` to get your barrings.

<!-- ### Offline **Builder** Docker Environment

Environment designed to build yannt sdist and wheel packages by running within a docker environment within an offline system (i.e. no internet). The Docker container is only for managing the build environment, all modified files (with the docker `/work` mount) happen on the host system. Dependencies are expected to be pre-collected from an internet connected system and then prestaged into the same output folder (`pip_pkgs`) in the offline system. 

To initialize, from top level `yannt` folder: `./scripts/build-docker-local-prod.sh`

Optionally, select a specific python version: `PY_VER=3.9 ./scripts/build-docker-local-prod.sh`

If successful, (assuming `python3 --version` is `3.13`) this will create: `./pip_pkgs/yannt/3.13` where all output ends up.

### Offline Developer Docker Environment

Environment designed to run within a docker environment within an offline system (i.e. no internet). The Docker container is only for managing the runtime environment, all modified files (with the docker `/work` mount) happen on the host system. Dependencies are expected to be precollected from an internet connected system and then prestaged into the same output folder (`pip_pkgs`) in the offline system. Docker environments are good for testing and developing with Python versions that are not available on the host system.

To initialize, from top level `yannt` folder: `./scripts/init-docker-local-dev.sh`

Optionally, select a specific python version: `PY_VER=3.9 ./scripts/init-docker-local-dev.sh`

If successful, (assuming `python3 --version` is `3.13`) this will create: `./pip_pkgs/3.13`, and `./venv/ml-venv-3.13-dld`.

You're terminal should also have a prefix: `(ml-venv-3.13-dld)`

### Online Developer Docker Environment

Environment designed to run within a docker environment within an online system (i.e. internet connected). The Docker container is only for managing the runtime environment, all modified files (with the docker `/work` mount) happen on the host system. In contrast to the Offline version, this environment will always attempt to initialize with the newest upstream packages allowed by the package dependency definitions. Docker environments are good for testing and developing with Python versions that are not available on the host system.

To initialize, from top level `yannt` folder: `./scripts/init-docker-upstream-dev.sh`

Optionally, select a specific python version: `PY_VER=3.9 ./scripts/init-docker-upstream-dev.sh`

If successful, (assuming `python3 --version` is `3.13`) this will create: `./pip_pkgs/3.13`, and `./venv/ml-venv-3.13-dud`.

You're terminal should also have a prefix: `(ml-venv-3.13-dud)`

### Offline Developer Host Environment

Environment designed to run directly on the current host environment, utilizing a system installed python environment. This host environment is offline compatible (i.e. no internet). Dependencies are expected to be precollected from an internet connected system and then prestaged into the same output folder (`pip_pkgs`) in the offline system.

To initialize, from top level `yannt` folder: `./scripts/init-host-local-dev.sh`

If successful, (assuming `python3 --version` is `3.13`) this will create: `./pip_pkgs/3.13`, and `./venv/ml-venv-3.13-hld`.

You're terminal should also have a prefix: `(ml-venv-3.13-hld)`

### Online Developer Host Environment

Environment designed to run directly on the current host environment, utilizing a system installed python environment. This host environment is expected to be online (i.e. internet connectivity). In contrast to the Offline version, this environment will always attempt to initialize with the newest upstream packages allowed by the package dependency definitions.

To initialize, from top level `yannt` folder: `./scripts/init-host-upstream-dev.sh`

If successful, (assuming `python3 --version` is `3.13`) this will create: `./pip_pkgs/3.13`, and `./venv/ml-venv-3.13-hud`.

You're terminal should also have a prefix: `(ml-venv-3.13-hud)` -->


