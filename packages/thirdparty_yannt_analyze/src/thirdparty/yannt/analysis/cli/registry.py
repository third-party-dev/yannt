"""Registry for analyze sub-commands, supporting direct registration and entry-point plugins."""

from importlib.metadata import entry_points
from typing import Callable, Iterable

CommandRegistrar = Callable[[object], None]

_COMMANDS: dict[str, CommandRegistrar] = {}

def register_command(name: str, registrar: CommandRegistrar) -> None:
    """Register a sub-command

    Args:
        name: Name for the command.
        registrar: Callable that attaches the sub-command to an argparse subparser.

    Raises:
        ValueError: If a different registrar is already registered under ``name``.
    """
    if name in _COMMANDS and _COMMANDS[name] != registrar:
        raise ValueError(f"Command '{name}' already registered")
    _COMMANDS[name] = registrar

def get_commands() -> Iterable[CommandRegistrar]:
    """Return all registered commands.

    Returns:
        List of registered CommandRegistrars.
    """
    return _COMMANDS.values()

def load_entrypoint_plugins(entrypoint_group: str = 'analyze_command') -> None:
    """Load register commands from defined entry points.

    Args:
        entrypoint_group: The entry point name (e.g. ``'analyze_command'``).
    """

    if isinstance(entry_points(), dict):
        # Python <3.10
        eps = []
        if entrypoint_group in entry_points():
            for ep in entry_points()[entrypoint_group]:
                if not ep in eps:
                    eps.append(ep)
    else:
        # Python >=3.10
        eps = entry_points(group=entrypoint_group)

    for ep in eps:
        register_command(ep.name, ep.load())

