import argparse
from thirdparty.yannt.registry import get_commands
from thirdparty.yannt.plugins import builtin
from thirdparty.yannt.plugins.loader import load_entrypoint_plugins

def main():
    parser = argparse.ArgumentParser(prog="yannt")
    subparsers = parser.add_subparsers(dest="command", required=True)

    load_entrypoint_plugins()

    # Load plugins
    for registrar in get_commands():
        registrar(subparsers)

    args = parser.parse_args()
    args.func(args)