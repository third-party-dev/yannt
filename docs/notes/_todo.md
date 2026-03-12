# TODO

- podman is a lie. Podman build requires /etc/subuid and /etc/subgid (which requires root!). podman run works fine without root, but the moment you want to use it for building an image, suddenly that is "special". WTF?!

  - As a result, to support containerization for _truely_ rootless setups, we need to "build" our podman containers with `podman run` instead of `podman build`. Ugh.

- Consider alternative python virtual environments that control interpreters:
  - uv, pyenv, (we already support conda)

- Re-integrate transformers
