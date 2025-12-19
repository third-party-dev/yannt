
- **Standard python build and install process for Yannt**

- Docker image for _developing_ yannt
  - Includes `pip install -e .` for internal stuff
  - Useful for inplace development cycles

- Docker image for _deploying_ yannt
  - All wheel/tar.gz installs
  - Also useful for testing standard build and install process.

- Working thoughts....


- Docker wrapper script will volume mount `/` to `/host`. Then /host`$(realpath $(pwd))` will be the working directory. All relative arguments should then work. Absolute paths will need the user to prepend `/host`. The wrapper code should be able to detect all arguments that start with `/`, see if its not `/host/` and warn the user before continuing.
