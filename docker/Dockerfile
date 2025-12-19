FROM debian:13-slim

RUN apt-get update && apt-get install -y \
    python3.13 python3-pip python3-venv git neovim curl

ARG VENV_PATH=/opt/ml-venv

RUN python3 -m venv $VENV_PATH \
    && $VENV_PATH/bin/pip install --upgrade pip setuptools wheel build pytest \
    && chmod -R a+rX $VENV_PATH

ENV PATH="$VENV_PATH/bin:$PATH"

# This one is weird
RUN pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cpu

# TODO: These should be managed by pyproject.toml
RUN pip install transformers
RUN pip install numpy
RUN pip install protobuf

# Note: Using sdist for version compatibility.
COPY *.tar.gz /opt/wheels/
RUN pip install /opt/wheels/*.tar.gz

# For contextual binaries and scripts
COPY bin/ /opt/ml-venv/bin/

WORKDIR /host

ENTRYPOINT ["yannt"]