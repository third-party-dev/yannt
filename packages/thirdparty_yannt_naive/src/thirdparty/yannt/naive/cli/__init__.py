import argparse
from thirdparty.yannt.naive.cli.registry import get_commands, load_entrypoint_plugins

def main():
    # Create parent parser
    parser = argparse.ArgumentParser(prog="naive")
    parser.add_argument("--breakpoint",
        dest="breakpoint",
        action="store_true",
        help="breakpoint() after operation"
    )
    subparsers = parser.add_subparsers(dest="naive_command", required=True)

    # Load the entrypoints
    load_entrypoint_plugins("naive_command")

    # Load plugins
    for registrar in get_commands():
        registrar(subparsers)

    args = parser.parse_args()
    args.func(args)