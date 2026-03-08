run CONFIG="" *args:
    ./scripts/run-dev.sh {{CONFIG}} -- {{args}}

init CONFIG="" *args:
    ./scripts/init-dev.sh {{CONFIG}} -- {{args}}