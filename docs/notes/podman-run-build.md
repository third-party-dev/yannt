# Podman Run Build

```sh
PODMAN="podman --root $(pwd)/cache/podman-runroot"
PY_VER=3.11
ML_VENV_NAME=yannt-py${PY_VER}-podman
RUN="$PODMAN exec ${ML_VENV_NAME}"

$PODMAN create --name $ML_VENV_NAME --userns=keep-id \
  -v $(pwd):/work/cache/docker-home -w /work \
  -e PY_VER=${PY_VER} -e HOME=/work \
  docker.io/library/python:${PY_VER}-slim

$RUN chown root /var/lib/apt/lists/partial
$RUN chown root /var/lib/apt/lists/auxfiles
$RUN chown root /var/cache/apt/archives/partial
$RUN chown root /var/log/apt

$RUN apt-get update
$RUN apt-get install -y vim unzip
$RUN useradd -m user
```
