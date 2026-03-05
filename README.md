# Yet Another Neural Net Tool (`yannt`)

Yannt aims to provide an analysis framework for deeper understanding of the anatomy of AI technologies in use.

It it worth noting that yannt itself is a light wrapper around a number of plugins that do the specific work. This fractured design was deliberate to all a minimal viable install for a user's specific use case. Minimal functionality can often be desired when dealing with very large dependencies (pytorch+cuda) or unintelligent dependency management (tensorflow).

## Pparse

Pparse is its own python package and has its own documentation, but its worth noting here that pparse is the heart of yannt's functionality. pparse aims to:

- Enable parsing of very large files (model files) that do not fit on a single machine's memory.
- Parse model files independent of the upstream frameworks. For example, not executing pickle when parsing a PyTorch file.
- Parse model files that have been truncated (corrupted). In this context, pparse aims to parse up to the point where the file becomes invalid and keeps all of the parsed state to that point without crashing. (Quite annoying when you know a piece of software has 90% of the file and dies because it can't verify something I never asked it to verify!)

## Project Layout

- **yannt** - Top project directory (not the python package top)
  - **bundles** - Ephemeral folder for holding git bundles, used for transferring backups to offline systems.
  - **cache** - Ephemeral folder for holding virtual development environments (conda, venv, docker home folders).
  - **configs** - Directory of used (supported?) virtual development environment configurations.
  - **docs** - Documentation
    - **manual** - Proper "manual" for rendering to HTML and PDF.
    - **notes** - Chicken scratch notes that I'm not ready to delete.
  - **extern** - Ephemeral folder for holding references to other yannt plugins (often git repos themselves). All folders in extern are assumed to be python packages and are installed in place when building a standard yannt development environment with `init-dev.sh`.
  - **models** - Ephemeral folder for holding various models on the system for testing and development.
  - **outputs** - Ephemeral yannt output folder.
  - **scripts** - Scripts for building development environments, testing, and building of yannt package suites.
  - **upstream** - Ephemeral folder for holding clones of upstream git repos used for developing and testing yannt.
  - **yannt** - The yannt python package distribution. (This is the top of the python package.)
  - **do** - (Janky) self contained version of `just` for use with the adjacent `Justfile`.
  - **Justfile** - Modern-ish version of Makefile with design principles for project management.
  - **create-bundle.sh** - A convenience script for creating git bundles.

## Build Conda Environment

Make sure you have `conda` in your path. The scripts use the path of `conda` to locate the `activate` script. If you do not have `conda` installed, you can install with similar to:

```sh
# Note: Roughly a 150M download
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh -b -p /opt/data/miniconda3
```

Note: Once you have conda installed, when you build a yannt environment, you may experience conda asking about terms of service (TOS) the first time you use the `defaults` channel and `conda-forge` channel. Accept the agreement and it the same prompt should not pop up with subsequent calls.

To build a yannt development environment with Conda, find an appropriate config to use in `configs/env` that ends with `-conda` and then (from the top `yannt` folder), run `./scripts/init-dev.sh $CONFIG_NAME`. For example:

```sh
./scripts/init-dev.sh py3.11-conda
```

Re-enter your conda environment without rebuilding by doing:

```sh
./scripts/run-dev.sh py3.11-conda
```

## Build Docker Environment

Make sure you have `docker` installed and can access the `docker` command as a user (ie make sure `whoami` is in the `docker` group.)

To build a yannt development environment with Conda, find an appropriate config to use in `configs/env` that ends with `-docker` and then (from the top `yannt` folder), run `./scripts/init-dev.sh $CONFIG_NAME`. For example:

```sh
./scripts/init-dev.sh py3.11-docker
```

Re-enter your docker environment without rebuilding by doing:

```sh
./scripts/run-dev.sh py3.11-docker
```

## Caching

For development stability and determinism, I "manually" cache all python packages in `cache/pip_pkgs` by running `pip download` before `pip install`. This has the side effect of _locking_ packages to the versions that are in that cache. Some may consider the locking a bad thing because if you don't specify versions in the requirements it should naturally update. I consider the locking _advantageous_ because I have positive control over what packages are available to the build. I also get a completely offline repo for free that I can transfer to isolated environments or use while offline.

To perform a natural update, update the requirements in `configs/pyver`, wipe the folder (or individual packages) from the folder corresponding to your python version, and re-run `init-dev.sh`. In my case, I wipe the entire `cache` folder and run `build-all.sh` to test all upstream-ed environments.

## My Rig

- I use Linux, not Windows.
- I use bash.
- I use Python 3.9 and later.
- I use Docker Community Edition.
- I use Debian Trixie (when I can) and Ubuntu 24 or later (when I can't use Debian).
- I do not install into system packages with pip. (venv with Docker, conda with host).

## Test Yolo Models

Managing environments with Ultralytics can be a nightmare. The yannt project includes two conda environments for using ultralytics and the `yolo` command. This can be quite useful for generating test models.

- For tensorflow based models (saved_model, tflite): `./scripts/init-dev.sh yolo-tf-conda`
- For all other models: `./scripts/init-dev.sh yolo-conda`

Example Yolo Commands:

```sh
# yolo-conda
yolo export model=yolov5su.pt format=torchscript
# yolo-conda, yolo-tf-conda
yolo export model=yolov5su.pt format=onnx
# yolo-conda
yolo export model=yolov5su.pt format=openvino
# yolo-conda
yolo export model=yolov5su.pt format=coreml
# yolo-tf-conda
yolo export model=yolov5su.pt format=saved_model
# yolo-tf-conda
yolo export model=yolov5su.pt format=tflite
# yolo-conda
yolo export model=yolov5su.pt format=paddle
# yolo-conda
yolo export model=yolov5su.pt format=ncnn
# NOT WORKING _GENERALLY_ (requires running CUDA driver)
yolo export model=yolov5su.pt format=engine
```
