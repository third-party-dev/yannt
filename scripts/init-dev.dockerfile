ARG PY_VER=3.9
ARG APT_PKGS=""
FROM python:${PY_VER}-slim
RUN apt-get update && apt-get install -y vim $APT_PKGS
RUN useradd -m user
