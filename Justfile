run CONFIG="" *args:
    ./scripts/run-dev.sh {{CONFIG}} -- {{args}}

init CONFIG="" *args:
    ./scripts/init-dev.sh {{CONFIG}} -- {{args}}

enable PLUGIN="":
    ./scripts/plugin-enable.sh {{PLUGIN}}

disable PLUGIN="":
    ./scripts/plugin-disable.sh {{PLUGIN}}

podman CONFIG="" *args:
    ./scripts/podman.sh {{CONFIG}} -- {{args}}