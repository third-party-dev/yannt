FROM python:3.13-slim AS builder

# RUN apt-get update && apt-get install -y \
#     python3.13 python3-pip python3-venv

ARG VENV_PATH=/opt/ml-venv

RUN python3 -m venv $VENV_PATH \
    && $VENV_PATH/bin/pip install --upgrade pip setuptools wheel build pytest \
    && chmod -R a+rX $VENV_PATH

ENV PATH="$VENV_PATH/bin:$PATH"

ARG PIP_INSTALL_FLAGS=""

# Copy all 
COPY pip_pkgs/ /opt/pip_pkgs/

# This one is weird
ARG TORCH_FLAGS="--index-url https://download.pytorch.org/whl/cpu"
RUN pip install $PIP_INSTALL_FLAGS torch torchaudio torchvision $TORCH_FLAGS

# TODO: These should be managed by pyproject.toml
RUN pip install $PIP_INSTALL_FLAGS transformers
RUN pip install $PIP_INSTALL_FLAGS numpy
RUN pip install $PIP_INSTALL_FLAGS protobuf

# Note: Using sdist for version compatibility.
COPY *.tar.gz /opt/pip_pkgs/
RUN pip install /opt/pip_pkgs/*.tar.gz

# ------------------------- The Real Docker Image -------------------------
FROM python:3.13-slim

ARG VENV_PATH=/opt/ml-venv
ENV PATH="$VENV_PATH/bin:$PATH"

# RUN apt-get update && apt-get install -y git curl \
#     && rm -rf /var/lib/apt/lists/*

# Copy binary out of the builder stage
COPY --from=builder $VENV_PATH $VENV_PATH

# For contextual binaries and scripts
COPY bin/ /opt/ml-venv/bin/

WORKDIR /host

ENTRYPOINT ["yannt"]