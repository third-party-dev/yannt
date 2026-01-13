ARG PY_VER="3.13"
FROM python:${PY_VER}-slim
RUN useradd -m user
