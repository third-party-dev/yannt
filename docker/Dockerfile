FROM python:3.13-slim AS builder

ARG VENV_PATH=/opt/ml-venv

# Copy all cached packages
COPY pip_pkgs/ /opt/pip_pkgs/
COPY local_pkgs/ /opt/local_pkgs/

RUN python3 -m venv $VENV_PATH \
    && $VENV_PATH/bin/pip install --no-index --find-links /opt/pip_pkgs/ \
        --upgrade pip setuptools wheel build pytest \
    && chmod -R a+rX $VENV_PATH

ENV PATH="$VENV_PATH/bin:$PATH"

RUN pip install --no-index --find-links /opt/pip_pkgs/ /opt/local_pkgs/*.tar.gz

# ------------------------- The Real Docker Image -------------------------
FROM python:3.13-slim

ARG VENV_PATH=/opt/ml-venv
ENV PATH="$VENV_PATH/bin:$PATH"

# Copy binary out of the builder stage
COPY --from=builder $VENV_PATH $VENV_PATH

# For contextual binaries and scripts
COPY bin/ /opt/ml-venv/bin/

WORKDIR /host

ENTRYPOINT ["yannt"]