import argparse

from thirdparty.yannt.cli.registry import register_command


def register(subparsers):
    # parser = subparsers.add_parser("_hello", help=argparse.SUPPRESS, usage=argparse.SUPPRESS)
    # parser.add_argument("--name", default="world")
    # parser.set_defaults(func=run)
    pass


def run(args):
    print(f"Hello, {args.name}!")


register_command("hello", register)
