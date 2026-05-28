#!/usr/bin/env python3

from pprint import pprint
from pathlib import Path
import os
import shlex

import yaml

class Executor:
    def emit(self, scripts: list[Script], ctx: BuildContext) -> BuildContext:
        raise NotImplementedError("abstract Executor.emit() not implemented")
    
    def _resolve_order(self, scripts: list[Script]) -> list[Script]:
        by_name = {s.name: s for s in scripts}
        visited = set()
        in_progress = set()
        ordered = []

        def visit(name: str):
            if name in visited:
                return
            if name in in_progress:
                raise ValueError(f"Circular dependency: {name}")
            
            in_progress.add(name)

            script = by_name.get(name)
            if script is None:
                raise ValueError(f"Script {name} not defined")
            
            for dep in script.depends_on:
                visit(dep)
            
            in_progress.discard(name)
            visited.add(name)
            ordered.append(script)
        
        for script in scripts:
            visit(script.name)
        
        return ordered


class Script:
    def __init__(self, name="unnamed.sh", body="", interpreter="/bin/sh", env={}, depends_on=[]):
        self.name = name
        self.body = body
        self.interpreter = interpreter
        self.env = env
        self.depends_on = depends_on

class BuildContext:
    def __init__(self, executor: Executor, config: dict): #, cache_dir: Path)
        self.executor = executor
        self.config = config

class Builder:
    def __init__(self, config: dict, child: Optional['Builder']):
        self.config = config
        self.child = child

    def emit_start(self, parent_cfg) -> Script:
        raise NotImplementedError("abstract Builder.emit_start() not implemented")

    def emit_scripts(self) -> list[Script]:
        raise NotImplementedError("abstract Builder.emit_scripts() not implemented")
    
    def get_name(self):
        layer_name = self.__class__.__name__
        if 'alias' in self.config:
            layer_name = self.config['alias']
        return layer_name


    def build(self, ctx: BuildContext):
        scripts = self.emit_scripts(ctx)
        inner_ctx = ctx.executor.stage_and_run(scripts, ctx)

        if self.child:
            self.child.build(inner_ctx)

class PodmanExecutor(Executor):
    def stage_and_run(self, scripts, ctx):
        ordered = self._resolve_order(scripts)
        for script in ordered:
            tmp = Path(f'/tmp/{script.name}')
            tmp.write_text(script.body)
            #subprocess.run(f'podman cp {tmp} {self.container_id}:/scripts/{script.name}.sh')
            #subprocess.run(f'podman exec ...',
            #env={**os.environ, **script.env})
        return ctx


class LinuxHostBuilder(Builder):
    def emit_start(self, parent_cfg, layer_dir) -> Script:
        # Emit scripts used to stage and run ourselves.
        raise NotImplementedError("LinuxHostBuilder.emit_start() not implemented")

    def emit_scripts(self, layer_dir) -> list[Script]:
        # Emit scripts used to setup this layer.

        return [
            Script(
                name="build.sh",
                body=f'#!/usr/bin/env bash\n./{layer_dir}/init-dev-podman.sh'
            )
        ]

        venv_path = self.config.get('path', '/opt/venv')
        


class PodmanBuilder(Builder):
    def emit_start(self, parent_cfg, layer_dir) -> Script:
        #from jinja2 import Environment, FileSystemLoader
        # env = Environment(loader=FileSystemLoader('./templates'))
        # template = env.get_template('mytemplate.sh.j2')
        # result = template.render(name="world", version="3.9")

        from jinja2 import Template, StrictUndefined
        template_path = Path("scripts") / "_" / "templates" / "init-dev-podman.sh.j2"
        template_data = open(template_path).read()

        self.config['layer_dir'] = layer_dir / self.get_name()

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

        return Script(
            name="init-dev-podman.sh",
            body=Template(template_data, undefined=StrictUndefined).render(**self.config)
        )

    def emit_scripts(self, layer_dir) -> list[Script]:

        from jinja2 import Template, StrictUndefined

        # TODO: Consider allowing user to override the download location for python packages.

        tmpl_path = {
            'download-all-deps.sh': Path("scripts") / "_" / "templates" / "download-all-deps.sh.j2",
            'run-dev-docker.sh': Path("scripts") / "_" / "templates" / "run-dev-docker.sh.j2",
            'build-venv.sh': Path("scripts") / "_" / "templates" / "build-venv.sh.j2",
            'linux-collection.sh': Path("scripts") / "_" / "templates" / "linux-collection.sh.j2",
        }
        tmpl_data = {
            'download-all-deps.sh': open(tmpl_path['download-all-deps.sh']).read(),
            'run-dev-docker.sh': open(tmpl_path['run-dev-docker.sh']).read(),
            'build-venv.sh': open(tmpl_path['build-venv.sh']).read(),
            'linux-collection.sh': open(tmpl_path['linux-collection.sh']).read(),
        }

        self.config['layer_path'] = layer_dir

        return [
            Script(
                name=name,
                body=Template(data, undefined=StrictUndefined).render(**self.config)
            )
            for name, data in tmpl_data.items()
        ]


class VenvBuilder(Builder):
    def emit_start(self, parent_cfg, layer_dir) -> Script:

        from jinja2 import Template, StrictUndefined
        template_path = Path("scripts") / "_" / "templates" / "start-venv.sh.j2"
        template_data = open(template_path).read()
        
        return Script(
            name="start-venv.sh",
            body=Template(template_data, undefined=StrictUndefined).render(**self.config)
        )

    def emit_scripts(self, layer_dir) -> list[Script]:
        venv_path = self.config.get('path', '/opt/venv')
        return [Script(name="test.sh", body=f"# venv builder script {venv_path} {self.config['env_name']}")]


class Resolution:

    def __init__(self, builder_cls: type[Builder], executor_cls: type[Executor], executor_kwargs: dict = {}):
        self.builder_cls = builder_cls
        self.executor_cls = executor_cls
        self.executor_kwargs = executor_kwargs
    
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
            "platform": lambda v: v in ("linux"),
            "runtime": lambda v: v == "podman",
        },
        resolution=Resolution(PodmanBuilder, PodmanExecutor),
        priority=10,
    ),
    Rule(
        predicates={
            "runtime": lambda v: v in ("venv"),
        },
        resolution=Resolution(VenvBuilder, PodmanExecutor),
        priority=10,
    ),
    Rule(
        predicates={
            "platform": lambda v: v in ("linux"),
        },
        resolution=Resolution(LinuxHostBuilder, PodmanExecutor),
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
            bootstrap = builder.child.emit_start(builder.config, layer_dir) #inner_layer_type=builder.child.layer_type)
            start_path = layer_dir / bootstrap.name
            start_path.write_text(bootstrap.body)
            start_path.chmod(0o755)

            self.emit(builder.child, current_dir=layer_dir)

# class_registry = {
#   'host': HostRouter,
#   'podman': PodmanRouter,
# #   'vars': VarsHandler,
# #   'apt_collect': AptCollectionHandler,
# #   'apt': AptHandler,
#   'virtualenv': VirtualEnvRouter,
# }

# from_registry = {
#   'env': FromEnvHandler,
# }

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

    # Do not permit inheritance of special attributes.
    for blocked_inheritance in ['alias', 'runtime']:
        if blocked_inheritance not in cfg and blocked_inheritance in effective_attrs:
            del effective_attrs[blocked_inheritance]

    #print(f"PARSE_CONFIG: {effective_attrs}\n")
    
    resolution = Resolution.resolve(effective_attrs)

    inner_cfg = cfg.pop('inner', None)
    child = parse_config(inner_cfg, inherited_attrs=effective_attrs) if inner_cfg else None

    return resolution.builder_cls(effective_attrs, child=child)


'''



export PIP_UPSTREAM_VERIFIERS=${PIP_UPSTREAM_VERIFIERS:-"https://download.pytorch.org/whl/cpu https://pypi.org/simple"}


'''


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



