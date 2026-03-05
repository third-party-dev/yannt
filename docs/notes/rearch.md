
## TODO

- ~~Add cache (i.e. home) folder~~
  - ~~.cache, .config, .keras, pip_pkgs, venv, .bash_history, .coverage~~

- User Install: (`pip install thirdparty_yannt thirdparty_pparse thirdparty_sysscan`)
  - Implicitly assumes online and grabs dependencies from upstream pip via `pyproject.toml`.
  - Does not implicitly install `extern` plugins.
  - Should not have constraints requirements.
  - transformers/yolo not intended for users.

- ~~Dev Install: (`./scripts/init-dev.sh 3.9-docker` or `./scripts/run-dev.sh 3.9-docker`)~~
  - ~~Implicitly assumes docker used for pre-download pip dependencies (`pip_pkgs`).~~
  - ~~Implicitly assumes docker for all venv things.~~
  - ~~Implicitly installs `extern` plugins in place.~~
  - ~~May explicitly provide config name (`configs/yannt/[config-name]/.env`)~~

- Add configs/ ... TBD
  - ~~./env/[config-name]/ - dev install config combination~~
  - ~~./pyver/[PY_VER]/{constraints,requirements}.txt~~
  - Add ./cri/[target]/ ... TBD

- Add build packages workflow.

- ~~Keep outputs/, upstream/  ... also both .gitignored~~

- Add cri plugin as built into yannt
  - transformers/yolo become venv configs?


--- our stuff ---
yannt pparse [args]
yannt sysscan [args]

--- their stuff ---
yannt cri transformers [args]
yannt cri yolo [args]


yannt cri - run yannt thing inside container
  yannt cri [target] - implicitly builds, inits, runs
  
cri-config (transformers)
PY_VER=3.9
PY_CONSTRAINTS=contraints-py39.txt
