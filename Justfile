run CONFIG="" *args:
    ./scripts/run-dev.sh {{CONFIG}} -- {{args}}

init CONFIG="" *args:
    ./scripts/init-dev.sh {{CONFIG}} -- {{args}}

enable PLUGIN="":
    ./scripts/auto-package.sh enable {{PLUGIN}}

disable PLUGIN="":
    ./scripts/auto-package.sh disable {{PLUGIN}}

enable-all:
    ./scripts/auto-package.sh enable-all

disable-all:
    ./scripts/auto-package.sh disable-all

podman CONFIG="" *args:
    ./scripts/podman.sh {{CONFIG}} -- {{args}}

# Source Maintenance Targets

bundle:
    ./scripts/create-bundle.sh

bundle-full:
    ./scripts/create-bundle-full.sh

buildpkgs TAG="":
    ./scripts/build-pkgs.sh {{TAG}}

buildenvs:
    ./scripts/build-all-envs.sh