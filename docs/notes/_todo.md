# TODO

## yannt

- podman is a lie. Podman build requires /etc/subuid and /etc/subgid (which requires root!). podman run works fine without root, but the moment you want to use it for building an image, suddenly that is "special". WTF?!

  - As a result, to support containerization for _truely_ rootless setups, we need to "build" our podman containers with `podman run` instead of `podman build`. Ugh.

- Consider alternative python virtual environments that control interpreters:
  - uv, pyenv, (we already support conda)

- Re-integrate `hft` as its own environment config.
  - Note: `hft` _does_ now get auto installed as a package via `./do enable-all`

- Provide full examples.

## Pparse

- Need a common way to dump node trees!
- Need to normalize node API across all parsers.
- Need to setup minimal test rigs for protobuf, flatbuffers, json, and pickle.
- Standardize the "make_*_parser" decorator pattern for all lazy parsers.

## Naive

- Consider using our own MNN and TFlite flatbuffers bindings for naive interface.