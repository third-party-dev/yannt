# Getting Started

** WIP **

When getting started with yannt, you need to know if you plan to interact with the code as a developer/builder or a user. If you are going to be in the developer/builder camp, you'll want to start with the "Developer Environment Setup" instructions. If you are going to be a user, please start with the instructions for Pipx Setup or Jupyter Setup.

There are a number of different ways to setup or use yannt. The follow sections will describe each. In summary:

- Jupyter
- Pipx
- Offline Developer Docker Environment
- Offline Developer Host Environment
- Online Developer Docker Environment
- Online Developer Host Environment
- Offline Builder Docker Environment

## Jupyter

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

Now you should have `yannt` as a command in your normal (user) system environment.

## Developer Environment Setup

To keep various capabilities independent and plugable, many components are divided up into their own repositories. Yannt is assumed to be at the top `./yannt` with all plugin source code cloned into yannt's extern folder `./yannt/extern/[plugin-pkg-name]`. The following commands should get you going (assuming bash-like shell):

```sh
# ! For _reasons_:
# ! - (atm) Assuming docker installed and current user has docker access.
# ! - (atm) Assuming systems has Python 3.13 (I'm using debian 13)
cd ~ ; mkdir thirdparty-ws ; cd thirdparty-ws
ln -s yannt/extern/thirdparty_pparse pparse
ln -s yannt/extern/thirdparty_yannt_transformers yannt_transformers
git clone https://github.com/third-party-dev/yannt.git
cd yannt ; mkdir extern ; cd extern
git clone https://github.com/third-party-dev/pparse.git thirdparty_pparse
git clone https://github.com/third-party-dev/yannt-transformers.git thirdparty_yannt_transformers
# ... git clone any additional plugins that you want to work with, using this convention ...
# go back to top yannt folder
cd ..
```

Once you have the environment cloned locally into the workspace (thirdparty-ws) or project (yannt) folders, you'll want to initialize the environment for developer activities. See the following sections for the options.

### Offline **Builder** Docker Environment

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

You're terminal should also have a prefix: `(ml-venv-3.13-hud)`

### Bash Tab Completion

As part of the developer virtual environment, bash tab completion is included for `yannt` command. As per the usual `argparse` enabled command, you can also run `yannt --help` to get your barrings.
