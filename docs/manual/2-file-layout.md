# Various File System Layouts

## Workspace Layout

- `thirdparty-ws` - The name of this folder can be anything, but I will normally name _workspace_ folders after the larger effort or epic that it is contributing too. Sometimes it becomes the forge organization.
- `thirdparty-ws/yannt` - Top level git repo folder for yannt.
- `thirdparty-ws/pparse` - A symlink to the yannt extern/thirdparty_pparse. Avoids having multiple checkouts that could get out of sync.
- `thirdparty-ws/yannt_transformers` - A symlink to the yannt extern/thirdparty_yannt_transformers. Avoids having multiple checkouts that could get out of sync.

When working on the individual plugins, I treat them as their own independent projects and _then_ test them with `yannt` integration.

When performing any virtual environment updates or resets, I always perform them from the `thirdparty-ws/yannt` folder so I can make assumptions like: "all in-place installs will exist in `extern` relative to `yannt` top folder.". 

## `thirdpart-ws/yannt` Project Layout

- `bundles` - Only appears when `create-bundle.sh` is run. For reasons, I've used `git bundles` to copy repo around. **Git Ignored**
- `docs` - Documentation folder with markdown content.
- `docs/pandoc-build` - Pandoc build source code for building the docs as a PDF. Symlinks to parent to access markdown.
- `extern` - In-place installs of (in development) yannt plugins. **Git Ignored**
- `pip_pkgs` - Downloaded pip dependency location (from running `./download.sh` in docker folder). **Git Ignored**
- `scripts` - Location of all initialization, collection, build, and install scripts.
- `upstream` - Folder for holding upstream source code (e.g. pytorch source code). **Git Ignored**
- `venv` - Location of all Python virtual environments. Note: Must be recreated if moved. **Git Ignored**
- `yannt` - The top folder for the yannt python package distribution.

## `thirdpart-ws/yannt/yannt` Package Distribution

- `yannt/pyproject.toml` - Descriptor for the yannt python package distribution.
- `yannt/src` - `pyproject.toml` is defined to only read source from the yannt `src` folder for the package.
- `yannt/src/thirdparty/yannt/cli` - Actual code responsible for discovering registered plugins and integrating them into yannt subcommands.
- `yannt/src/thirdparty/yannt/plugins` - (unused) stub code for including _builtin_ plugins. In all cases thus far, I'd prefer to manage plugins as python package distributions that register yannt package entry points.
