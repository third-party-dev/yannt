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

- ~~Need a common way to dump node trees!~~
- ~~Need to normalize node API across all parsers.~~
- ~~Need to setup minimal test rigs for protobuf, flatbuffers, json, and pickle.~~
- Standardize the "make_*_parser" decorator pattern for all lazy parsers.

- ~~Consider allowing file offsets in CLI/view objects for analysis work.~~
  - For now, we can recreate the file with `dd`. Ideally, we should be able to point FileData to an offset.

- ~~Consider a breadth first (per node) flatbuffers parser for pparse.~~
  - ~~When given a vector, pre-generate the uninitialized element node object for all elements in the vector. THEN go through each and parse. Note: Flatbuffers is ideal for deferred parsing (when not doing discovery)!~~

- RKNN
  - Grab a clean graph and calculate hash.
  - Grab clean tensor data from pt or onnx file.
  - Investigate tensor data with a known good graph.
  - Investigate parsing rknn via rknntoolkit shared object.

- Consider a base class for StreamParser and base class for DiskParser

### New Features (after 0.0.4)

- Control Recursion

- ~~Provide URLDataSource~~

- Analyzers (per extraction)
  - Layer Count, Activation ID

- Test on Windows

- Export / Import State
  - DataSource
  - Extractions
    - IDed by sha1sum + length
  - Parser Options
  - NodeTree Nodes
  - Optionally NodeTree Contexts

- SafeTensors + Graph
  - Convert NodeTree to "GiSt".
  - (Some) Analyzers should read GiSt.
  - **BLOCKER**: SafeTensors `__metadata__` only allows Dict[str, str]. `:(`

- Serialize
  - Fresh (hard)
  - Overlay (easy)

## Naive

- Consider using our own MNN and TFlite flatbuffers bindings for naive interface.
- For proprietary formats (OM, MNN, RKNN), we should consider comparing pre-conversion to parsed for testing. Naive at that point becomes loading the open version (onnx) and then possible transform/conversion to the unparsable via "naive".
  - In summary, have naive: parsing, transforms, and IR dumps.

## Misc

- AL uses FILTER, EXTRACT, CORE, SECONDARY, POST, REVIEW per file.

- pparse (conceptually) uses Filter, Parse, Analyze, Alter, Serialize, but not as automated pipeline.
