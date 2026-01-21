ARG PY_VER="3.13"
FROM python:${PY_VER}-slim
RUN apt-get update && apt-get install -y graphviz
RUN useradd -m user
