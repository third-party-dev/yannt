
## TODO

- Add cache (i.e. home) folder
  - .cache, .config, .keras, pip_pkgs, venv, .bash_history, .coverage

- User Install: (`pip install thirdparty_yannt thirdparty_pparse thirdparty_sysscan`)
  - Implicitly assumes online and grabs dependencies from upstream pip via `pyproject.toml`.
  - Does not implicitly install `extern` plugins.
  - Should not have constraints requirements.

- Dev Install: (`./scripts/init-dev.sh 3.9-docker` or `./scripts/run-dev.sh 3.9-docker`)
  - Implicitly assumes docker used for pre-download pip dependencies (`pip_pkgs`).
  - Implicitly assumes docker for all venv things.
  - Implicitly installs `extern` plugins in place.
  - May explicitly provide config name (`configs/yannt/[config-name]/.env`)

- Add configs/ ... TBD
  - ./yannt/target/[config-name]/ - dev install config combination
  - ./yannt/version/[PY_VER]/{constraints,requirements}.txt
  - ./yannt/docker-dev
  - ./yannt/host-dev
  - Add ./cri/[target]/ ... TBD

- Keep outputs/, upstream/  ... also both .gitignored

- Add cri plugin as built into yannt
  - transformers and yolo become container specific -> TBD



env-config
PY_VER=3.9
PY_CONSTRAINTS=contraints-py39.txt

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
