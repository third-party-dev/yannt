from typing import Callable, Dict

CommandRegistrar = Callable[[object], None]

_COMMANDS: Dict[str, CommandRegistrar] = {}

def register_command(name: str, registrar: CommandRegistrar):
    if name in _COMMANDS:
        raise ValueError(f"Command '{name}' already registered")
    _COMMANDS[name] = registrar

def get_commands():
    return _COMMANDS.values()