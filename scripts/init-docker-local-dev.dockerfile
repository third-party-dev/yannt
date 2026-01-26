ARG PY_VER="3.13"
FROM python:${PY_VER}-slim
RUN apt-get update && apt-get install -y \
  graphviz flatbuffers-compiler protobuf-compiler
RUN useradd -m user
