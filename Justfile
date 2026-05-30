run CONFIG="" *args:
    @./scripts/run-dev.sh {{CONFIG}} -- {{args}}

init CONFIG="" *args:
    @./scripts/init-dev.sh {{CONFIG}} -- {{args}}

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

bundle DURATION="":
    ./scripts/create-bundle.sh {{DURATION}}

builddevpkgs TAG="":
    ./scripts/build-dev-pkgs.sh {{TAG}}

builddevpparse TAG="":
    cd packages/thirdparty_pparse && ./scripts/build-dev-pkgs.sh {{TAG}}

buildpkgs TAG="":
    ./scripts/build-pkgs.sh {{TAG}}

buildpparse TAG="":
    cd packages/thirdparty_pparse && ./scripts/build-pkgs.sh {{TAG}}

buildenvs:
    ./scripts/build-all-envs.sh

pytests *args:
    ./scripts/pytests.sh {{args}}