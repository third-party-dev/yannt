import argparse
from thirdparty.yannt.cli.registry import get_commands, load_entrypoint_plugins
from thirdparty.yannt.plugins import builtin

def main():
    parser = argparse.ArgumentParser(prog="yannt")
    subparsers = parser.add_subparsers(dest="yannt_command", required=True)

    load_entrypoint_plugins("yannt_command")

    # Load plugins
    for registrar in get_commands():
        registrar(subparsers)

    args = parser.parse_args()
    args.func(args)