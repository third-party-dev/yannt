ARG PY_VER=3.9
ARG APT_PKGS=""
FROM docker.io/library/python:${PY_VER}-slim

# Hack permitting podman runRoot to work on NFS mounts.
RUN chown root /var/lib/apt/lists/partial
    && chown root /var/lib/apt/lists/auxfiles
    && chown root /var/cache/apt/archives/partial
    && chown root /var/log/apt

RUN apt-get update && apt-get install -y vim $APT_PKGS
RUN useradd -m user
