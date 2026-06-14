import argparse
from thirdparty.yannt.analysis.cli.registry import get_commands, load_entrypoint_plugins


# Function called when the scripts CLI entry point is called.
def main() -> None:
    # Create parent parser
    parser = argparse.ArgumentParser(prog="analyze")
    parser.add_argument("--breakpoint",
        dest="breakpoint",
        action="store_true",
        help="breakpoint() after operation"
    )
    subparsers = parser.add_subparsers(dest="analyze_command", required=True)

    # Load the entrypoints
    load_entrypoint_plugins("analyze_command")

    # Load plugins
    for registrar in get_commands():
        registrar(subparsers)

    args = parser.parse_args()
    args.func(args)