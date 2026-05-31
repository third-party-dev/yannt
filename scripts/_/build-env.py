#!/usr/bin/env python3

from pprint import pprint # useful for breakpoint()
from pathlib import Path
import os

from collections.abc import Callable
from typing import Any

# For yannt-venv-py3.9:
#   docker run -ti -v $(pwd):/opt/yannt debian:11 bash
#   apt-get update && apt-get install -y python3 python3-yaml python3-jinja2 python3-venv curl
# For yannt-venv-py3.11:
#   docker run -ti -v $(pwd):/opt/yannt debian:12 bash
#   apt-get update && apt-get install -y python3 python3-yaml python3-jinja2 python3-venv curl
# For yannt-venv-py3.13:
#   docker run -ti -v $(pwd):/opt/yannt debian:13 bash
#   apt-get update && apt-get install -y python3 python3-yaml python3-jinja2 python3-venv curl

class Script:
    def __init__(self, name="unnamed.sh", body="", interpreter="/bin/sh", env={}, depends_on=[]):
        self.name = name
        self.body = body
        self.interpreter = interpreter
        self.env = env
        self.depends_on = depends_on


class Builder:
    def __init__(self, config: dict, inner_cfg): #child: Optional['Builder']):
        self.config = config
        self.child = parse_config(inner_cfg, inherited_attrs=self.override_inheritance(config)) if inner_cfg else None


    def override_inheritance(self, config):
        return config


    def emit_scripts(self) -> list[Script]:
        raise NotImplementedError("abstract Builder.emit_scripts() not implemented")


    def common_config_fixups(self, builder_path):
        self.config['YOU_CAN_EDIT_THIS_FILE'] = '# === DO NOT EDIT. Auto generated file. Edit the template. === #'
        self.config['builder_path'] = builder_path
        self.config['next_init_target'] = ''
        self.config['next_run_target'] = ''
        if self.child and 'init' in self.child.config:
            self.config['next_init_target'] = Path(builder_path) / self.child.get_name() / self.child.config['init']
        if self.child and 'run' in self.child.config:
            self.config['next_run_target'] = Path(builder_path) / self.child.get_name() / self.child.config['run']


    def get_name(self):
        layer_name = self.__class__.__name__
        if 'alias' in self.config:
            layer_name = self.config['alias']
        return layer_name


class LinuxHostBuilder(Builder):
    def emit_scripts(self, builder_path) -> list[Script]:
        from jinja2 import Template, StrictUndefined

        tmpl_paths = {
            'init-host.sh': Path("scripts/_/templates/host") / "init-host.sh.linux.j2",
        }
        tmpl_data = {tgt_fname: open(tmpl_path).read() for tgt_fname, tmpl_path in tmpl_paths.items()}

        # TODO: Make this implicit
        self.config['YOU_CAN_EDIT_THIS_FILE'] = '# === DO NOT EDIT. Auto generated file. Edit the template. === #'
        self.config['builder_path'] = builder_path
        self.config['next_init_target'] = ''
        self.config['next_run_target'] = ''
        if self.child and 'init' in self.child.config:
            self.config['next_init_target'] = Path(builder_path) / self.child.get_name() / self.child.config['init']
        if self.child and 'run' in self.child.config:
            self.config['next_run_target'] = Path(builder_path) / self.child.get_name() / self.child.config['run']

        return [
            Script(
                name=name,
                body=Template(data, undefined=StrictUndefined).render(**self.config)
            )
            for name, data in tmpl_data.items()
        ]


class PodmanBuilder(Builder):
    def override_inheritance(self, config):
        return {**config, 'proj_path': config['cri_proj_path']}


    def emit_scripts(self, builder_path) -> list[Script]:
        from jinja2 import Template, StrictUndefined

        # TODO: Consider allowing user to override the download location for python packages.

        tmpl_paths = {
            'init-podman.sh': Path("scripts/_/templates/podman") / "init-podman.sh.j2",
            'run-podman.sh': Path("scripts/_/templates/podman") / "run-podman.sh.j2",
            # out of date
            #'init-dev-podman.sh': Path("scripts") / "_" / "templates" / "init-dev-podman.sh.j2",
            #'download-all-deps.sh': Path("scripts") / "_" / "templates" / "download-all-deps.sh.j2",
            #'run-dev-docker.sh': Path("scripts") / "_" / "templates" / "run-dev-docker.sh.j2",
            #'build-venv.sh': Path("scripts") / "_" / "templates" / "build-venv.sh.j2",
            #'linux-collection.sh': Path("scripts") / "_" / "templates" / "linux-collection.sh.j2",
        }
        tmpl_data = {tgt_fname: open(tmpl_path).read() for tgt_fname, tmpl_path in tmpl_paths.items()}

        # Normalize attributes for template use.

        if 'extra_preapt_commands' in self.config and isinstance(self.config['extra_preapt_commands'], list):
            self.config['extra_preapt_commands'] = '\n    '.join(self.config['extra_preapt_commands'])
        elif 'extra_preapt_commands' not in self.config:
            self.config['extra_preapt_commands'] = ''

        if 'extra_podman_run_commands' in self.config and isinstance(self.config['extra_podman_run_commands'], list):
            self.config['extra_podman_run_commands'] = '\n    '.join(self.config['extra_podman_run_commands'])
        elif 'extra_podman_run_commands' not in self.config:
            self.config['extra_podman_run_commands'] = ''

        if 'apt_packages' in self.config and isinstance(self.config['apt_packages'], list):
            self.config['apt_packages'] = ' '.join(self.config['apt_packages'])
        elif 'apt_packages' not in self.config:
            self.config['apt_packages'] = ''

        # TODO: Make this implicit
        self.common_config_fixups(builder_path)

        return [
            Script(
                name=name,
                body=Template(data, undefined=StrictUndefined).render(**self.config)
            )
            for name, data in tmpl_data.items()
        ]


class LinuxPythonEnv(Builder):
    def emit_scripts(self, builder_path) -> list[Script]:
        from jinja2 import Template, StrictUndefined

        tmpl_paths = {
            'init-python.sh': Path("scripts") / "_" / "templates" / "python" / "init-python.sh.linux.j2",
            'download-pkgs.sh': Path("scripts") / "_" / "templates" / "python" / "download-pkgs.sh.linux.j2",
            'run-python.sh': Path("scripts") / "_" / "templates" / "python" / "run-python.sh.linux.j2",
            'build-venv.sh': Path("scripts") / "_" / "templates" / "python" / "build-venv.sh.linux.j2",
            'start-venv.sh': Path("scripts") / "_" / "templates" / "python" / "start-venv.sh.linux.j2",
        }
        tmpl_data = {tgt_fname: open(tmpl_path).read() for tgt_fname, tmpl_path in tmpl_paths.items()}

        # TODO: Make this implicit
        self.common_config_fixups(builder_path)

        return [
            Script(
                name=name,
                body=Template(data, undefined=StrictUndefined).render(**self.config)
            )
            for name, data in tmpl_data.items()
        ]


class WinePythonEnv(Builder):
    def emit_scripts(self, builder_path) -> list[Script]:
        from jinja2 import Template, StrictUndefined

        tmpl_paths = {
            'init-python.sh': Path("scripts") / "_" / "templates" / "python" / "init-python.sh.wine.j2",
            'download-pkgs.sh': Path("scripts") / "_" / "templates" / "python" / "download-pkgs.sh.wine.j2",
            'run-python.sh': Path("scripts") / "_" / "templates" / "python" / "run-python.sh.wine.j2",
            'build-venv.sh': Path("scripts") / "_" / "templates" / "python" / "build-venv.sh.wine.j2",
            'start-venv.sh': Path("scripts") / "_" / "templates" / "python" / "start-venv.sh.wine.j2",
        }
        tmpl_data = {tgt_fname: open(tmpl_path).read() for tgt_fname, tmpl_path in tmpl_paths.items()}

        # Morph PROJ_PATH into WINE_PROJ_PATH
        from pathlib import PurePosixPath, PureWindowsPath
        self.config['wine_proj_path'] = f"{self.config['root_drive']}{self.config['proj_path']}"

        # TODO: Make this implicit
        self.common_config_fixups(builder_path)

        return [
            Script(
                name=name,
                body=Template(data, undefined=StrictUndefined).render(**self.config)
            )
            for name, data in tmpl_data.items()
        ]


class Resolution:

    def __init__(self, builder_cls: type[Builder]): #, executor_cls: type[Executor], executor_kwargs: dict = {}):
        self.builder_cls = builder_cls
        # self.executor_cls = executor_cls
        # self.executor_kwargs = executor_kwargs
    
    @classmethod
    def resolve(cls, config: dict) -> "Resolution":
        matches = [
            rule for rule in Resolution.RULES
            if all(
                key in config and pred(config[key])
                for key, pred in rule.predicates.items()
            )
        ]
        if not matches:
            raise ValueError(f"No rule to match: {config}")

        # Optionally blocking ambiguity at the moment. Negates priority usage.
        #if len(matches) > 1:
        #    raise ValueError(f"Ambiguous resolution: {config}")
        
        return max(matches, key=lambda r: r.priority).resolution


class Rule:
    def __init__(self, predicates: dict[str, Callable[[Any], bool]], resolution: Resolution, priority: int = 0):
        self.predicates = predicates
        self.resolution = resolution
        self.priority = priority


Resolution.RULES = [
    Rule(
        predicates={
            "builder": lambda v: v == "host",
            "platform": lambda v: v == "linux",
        },
        resolution=Resolution(LinuxHostBuilder),
    ),
    Rule(
        predicates={
            "builder": lambda v: v == "podman",
            # implicitly linux
        },
        resolution=Resolution(PodmanBuilder),
    ),
    Rule(
        predicates={
            "builder": lambda v: v == "python",
            "platform": lambda v: v == "linux",
        },
        resolution=Resolution(LinuxPythonEnv),
    ),
    Rule(
        predicates={
            "builder": lambda v: v == "python",
            "platform": lambda v: v in "wine",
        },
        resolution=Resolution(WinePythonEnv),
    ),
]


class Emitter:
    def __init__(self, staging_dir: Path):
        self.staging_dir = staging_dir
    
    def emit(self, builder: Builder, current_dir: Path = None):
        if current_dir is None:
            current_dir = self.staging_dir
        
        # Note: Don't use runtime, layer depends on many factors.
        layer_name = builder.get_name()
        layer_dir = current_dir / layer_name
        layer_dir.mkdir(parents=True, exist_ok=True)

        for i, script in enumerate(builder.emit_scripts(layer_dir)):
            path = layer_dir / f"{script.name}"
            path.write_text(script.body)
            path.chmod(0o755)
        
        if builder.child:
            self.emit(builder.child, current_dir=layer_dir)


class FromEnvHandler:
    @classmethod
    def resolve(cls, cfg):
        if 'name' in cfg:
            if 'default' in cfg:
                return os.getenv(cfg['name'], cfg['default'])
            else:
                return os.getenv(cfg['name'])
        raise Exception(f"From without name: {cfg}")


FROM_REGISTRY = {
  'env': FromEnvHandler,
}


def resolve_value(cfg, attr):
    if attr in cfg:
        if list(cfg[attr].keys())[0] == 'from':
            return FROM_REGISTRY[cfg[attr]['from']].resolve(cfg[attr])
        else:
            return cfg[attr]


def parse_config(cfg: dict, inherited_attrs: dict = {}) -> Builder:

    # resolve current level config attributes
    for key in list(cfg.keys()):
        # if cfg[key] is a dict
        if isinstance(cfg[key], dict):
            # and its first key is from
            if list(cfg[key].keys())[0] == 'from':
                # resolve the value
                cfg[key] = FROM_REGISTRY[cfg[key]['from']].resolve(cfg[key])

    effective_attrs = {**inherited_attrs, **cfg}

    # TODO: Block dynamically clobbered attributes.
    # ['next_init_target', 'builder_path']

    # Do not permit inheritance of special attributes.
    for blocked_inheritance in ['alias', 'builder', 'init', 'inner']:
        if blocked_inheritance not in cfg and blocked_inheritance in effective_attrs:
            del effective_attrs[blocked_inheritance]
    
    resolution = Resolution.resolve(effective_attrs)

    inner_cfg = cfg.pop('inner', None)

    return resolution.builder_cls(effective_attrs, inner_cfg=inner_cfg)


def main():

    import argparse

    parser = argparse.ArgumentParser(description='My tool')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--init', action='store_true', help='initialize environment')
    group.add_argument('--run', action='store_true', help='run command')
    parser.add_argument('--extra', action='store')

    # TODO: This might be optional?
    parser.add_argument('--proj_path', action='store', required=True)
    parser.add_argument('--config_name', action='store', required=True)
    parser.add_argument('--config_path', action='store', required=True)

    args = parser.parse_args()

    extra = ''
    if args.extra:
        extra = json.loads(extra)

    # TODO: This might be optional?
    os.environ['PROJ_PATH'] = args.proj_path
    os.environ['CONFIG_NAME'] = args.config_name
    os.environ['CONFIG_PATH'] = args.config_path

    if args.init:

        import yaml

        # Test with: (. ./configs/env/yannt-py3.9-podman-wine/config ; ./scripts/_/build-env.py)
        with open(Path(os.getenv('CONFIG_PATH')) / 'plan.yaml', "r") as plan_fobj:
            root_builder = parse_config(yaml.safe_load(plan_fobj.read())['config_root'])

        staging = Path('cache') / 'builder' / root_builder.config['env_name']
        staging.mkdir(parents=True, exist_ok=True)

        emitter = Emitter(staging)
        emitter.emit(root_builder)

    if args.run:
        print(f"RUN: {extra}")


if __name__ == "__main__":
    main()






























































# class Builder:
#     def __init__(self, config: dict, child: Optional['Builder']):
#         self.config = config
#         self.child = child


#     def emit_scripts(self) -> list[Script]:
#         raise NotImplementedError("abstract Builder.emit_scripts() not implemented")


#     def get_name(self):
#         layer_name = self.__class__.__name__
#         if 'alias' in self.config:
#             layer_name = self.config['alias']
#         return layer_name


#     # def build(self, ctx: BuildContext):
#     #     scripts = self.emit_scripts(ctx)
#     #     inner_ctx = ctx.executor.stage_and_run(scripts, ctx)

#     #     if self.child:
#     #         self.child.build(inner_ctx)


# class BuildContext:
#     def __init__(self, executor: Executor, config: dict): #, cache_dir: Path)
#         self.executor = executor
#         self.config = config


# raw_yaml = '''
# config_root:
#   alias: host
#   platform: linux

#   proj_path: { from: env, name: PROJ_PATH }
#   config_path: { from: env, name: CONFIG_PATH }
#   config_name: { from: env, name: CONFIG_NAME }

#   py_ver: { from: env, name: PY_VER }
#   env_name: { from: env, name: ML_VENV_NAME }

#   inner:
#     alias: podman
#     runtime: podman
#     platform: linux
#     image: ubuntu:22.04

#     extra_preapt_commands:
#     - RUN dpkg --add-architecture i386

#     apt_packages:
#     - graphviz
#     - flatbuffers-compiler
#     - protobuf-compiler
#     - cmake
#     - build-essential
#     - wine
#     - wine32
#     - wine64
#     - wget
#     - ca-certificates

#     extra_podman_run_commands:
#     - RUN wineboot --init
#     - RUN wine reg add "HKEY_LOCAL_MACHINE\\\\System\\\\CurrentControlSet\\\\Control\\\\Session Manager\\\\Environment" /v Path /t REG_EXPAND_SZ /d "C:\\Python39;C:\\Python39\\Scripts" /f
#     - RUN wineserver --wait

#     ps1_tag: { from: env, name: PS1_TAG }
#     cri_home: { from: env, name: CRI_HOME }
#     cri_root: { from: env, name: CRI_ROOT }
#     cri_bin: { from: env, name: CRI_BIN }
#     cri_run: { from: env, name: CRI_RUN }
#     cri_run_args: { from: env, name: CRI_RUN_ARGS }
#     cri_proj_path: { from: env, name: CRI_PROJ_PATH }

#     python: { from: env, name: PYTHON }
#     pip_idx_args: { from: env, name: PIP_IDX_ARGS }
#     pip_upstream_verifiers: { from: env, name: PIP_UPSTREAM_VERIFIERS }
#     venv_python: { from: env, name: VENV_PYTHON }
#     py_constraints: { from: env, name: PY_CONSTRAINTS }
#     py_reqs: { from: env, name: PY_REQS }
#     pkg_skip_list: { from: env, name: PKG_SKIP_LIST }

#     inner:
#         runtime: venv
#         path: /opt/myenv
#         packages: [numpy, pandas]
# '''


# class Executor:
#     def emit(self, scripts: list[Script], ctx: BuildContext) -> BuildContext:
#         raise NotImplementedError("abstract Executor.emit() not implemented")
    
#     def _resolve_order(self, scripts: list[Script]) -> list[Script]:
#         by_name = {s.name: s for s in scripts}
#         visited = set()
#         in_progress = set()
#         ordered = []

#         def visit(name: str):
#             if name in visited:
#                 return
#             if name in in_progress:
#                 raise ValueError(f"Circular dependency: {name}")
            
#             in_progress.add(name)

#             script = by_name.get(name)
#             if script is None:
#                 raise ValueError(f"Script {name} not defined")
            
#             for dep in script.depends_on:
#                 visit(dep)
            
#             in_progress.discard(name)
#             visited.add(name)
#             ordered.append(script)
        
#         for script in scripts:
#             visit(script.name)
        
#         return ordered


# class PodmanExecutor(Executor):
#     def stage_and_run(self, scripts, ctx):
#         ordered = self._resolve_order(scripts)
#         for script in ordered:
#             tmp = Path(f'/tmp/{script.name}')
#             tmp.write_text(script.body)
#             #subprocess.run(f'podman cp {tmp} {self.container_id}:/scripts/{script.name}.sh')
#             #subprocess.run(f'podman exec ...',
#             #env={**os.environ, **script.env})
#         return ctx