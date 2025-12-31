import argparse
from thirdparty.yannt.cli.registry import get_commands, load_entrypoint_plugins
from thirdparty.yannt.plugins import builtin
import argcomplete
import sys

def main():
    parser = argparse.ArgumentParser(prog="yannt")
    subparsers = parser.add_subparsers(dest="yannt_command", required=True)

    load_entrypoint_plugins("yannt_command")

    # Load plugins
    for registrar in get_commands():
        registrar(subparsers)

    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    args.func(args)


# def dump_parser_actions(parser, depth=0):
#     indent = ' ' * depth
#     for action in parser._actions:
#         if isinstance(action, argparse._StoreAction):
#             #print(f'{indent}- Store Actions:')
#             if hasattr(action, "real_vfs_path"):
#                 print(f"{indent}  Found path argument: {action}")
#         if isinstance(action, argparse._SubParsersAction):
#             #print(f"{indent}- Subparsers:")
#             for choice_key, parser_value in action.choices.items():
#                 #print(f"{indent} - {choice_key}")
#                 dump_parser_actions(parser_value, depth+2)

