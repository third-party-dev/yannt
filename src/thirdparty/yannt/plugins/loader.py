from importlib.metadata import entry_points
from thirdparty.yannt.registry import register_command

def load_entrypoint_plugins():
    eps = entry_points(group="yannt.commands")
    for ep in eps:
        register = ep.load()
        register_command(ep.name, register)