# Notes

In previous iterations I attempted to have all dependencies and all things in a single build setup. I'm now discovering that the possibility of that happening is near-zero and the maintenance of that kind of setup is not tenable.

- Ultralytics dependencies, depending on the needs of the yolo command (and mostly tensorflow is to blame), are so tightly coupled that it ?*has* to be kept separate.
- Solutions for separation of environments are different amongst users and only those environment should be supported.
- We don't want to require users to install everything to do something simple. They should always only have to install what they need within a reasonable maintenance cost scheme. (i.e. not all users can simply use docker).

## Alternate Plan

At the moment, yannt has a config based setup with environment variables and python based configs. I think that this is the correct way to manage building environments, but we need to adjust what the output goals are.

The goal for environment management will be:

- Plain host based installations provide little value and should be avoided in all development situations. Instead of a plain host install, always use conda, docker, and/or venv. All plain host environment setups should be based on pre-built wheels or source packages.

- When environment scripts are run, they exec a shell that ends up in the resulting environment. A simple exit should remove the environment. yannt will not be in the game of "sourcing" in environment into existing shells.

- Docker - With python version specified
  - HOME will be ./cache/docker-home

- Conda - With python version specified
  - If we want to use conda inside of docker, the outer docker will not be managed. Developers should be able to utilize the yannt docker environment.
  - Environments will be specified to be in ./cache/conda/envs

## Use Cases

### Developer initializes Docker dev environment

### Developer initializes Conda dev environment