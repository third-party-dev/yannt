# Various File System Layouts

## Workspace Layout

- **thirdparty-ws** - The name of this folder can be anything, but I will normally name _workspace_ folders after the larger effort or epic that it is contributing too. Sometimes it becomes the forge organization.
- **thirdparty-ws/yannt** - Top level git repo folder for yannt.

Note: When performing any virtual environment updates or resets, I always perform them from the `thirdparty-ws/yannt` folder so I can make assumptions like: "all in-place installs will exist in `enabled` relative to `yannt` top folder.".

## **thirdpart-ws/yannt** Project Layout

- **bundles** - Ephemeral folder for holding git bundles, used for transferring backups to other systems.
- **cache** - Ephemeral folder for holding virtual development environment state (conda, venv, docker home folders).
  - **conda** - Project local storage for conda environments.
  - **docker/home** - A home directory for container users to save bash history and other caches.
  - **empty-context** - An always empty folder that can be used for empty docker contexts.
  - **pip_pkgs** - Project local pip package cache built with `pip download`.
  - **venv** - Project local storage for python virtual environments.
  - **podman/home** - A home directory for container users to save bash history and other caches.
  - **podman/runroot** - Project specific image cache and state database for podman.
- **configs** - Directory of virtual development environment configurations.
- **docs** - Documentation
  - **manual** - Proper "manual" for rendering to HTML and PDF.
  - **notes** - Chicken scratch notes that I'm not ready to delete.
- **enabled** - Ephemeral folder for holding references to yannt plugins that will be automatically installed in place when initializing a development environment.
- **models** - Ephemeral folder for holding various models on the system for testing and development.
- **outputs** - Ephemeral yannt output folder.
- **plugins** - Folder for storage of all plugin code (regardless of whether its in use).
- **scripts** - Scripts for building development environments, testing, and building of yannt package suites.
- **upstream** - Ephemeral folder for holding clones of upstream git repos used for developing and testing yannt.
- **yannt** - The yannt python package distribution. (This is the top of the python package.)
- **do** - (Janky) self contained version of `just` for use with the adjacent `Justfile`.
- **Justfile** - Modern-ish version of Makefile with design principles for project management.
- **create-bundle.sh** - A convenience script for creating git bundles.

## `thirdpart-ws/yannt/yannt` Package Distribution

- `yannt/pyproject.toml` - Descriptor for the yannt python package distribution.
- `yannt/src` - `pyproject.toml` is defined to only read source from the yannt `src` folder for the package.
- `yannt/src/thirdparty/yannt/cli` - Actual code responsible for discovering registered plugins and integrating them into yannt subcommands.
- `yannt/src/thirdparty/yannt/plugins` - (unused) stub code for including _builtin_ plugins. In all cases thus far, I'd prefer to manage plugins as python package distributions that register yannt package entry points.
