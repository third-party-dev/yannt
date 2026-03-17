'''
def register(subparsers):
    p = subparsers.add_parser("foo", help="Foo command")
    p.add_argument("--x", type=int, required=True)
    p.set_defaults(func=run)

def run(args):
    print(args.x * 2)
'''

from thirdparty.yannt.naive.cli.registry import get_commands, load_entrypoint_plugins

def register_naive(subparsers):
    naive_parser = subparsers.add_parser("naive", help="naive command")
    naive_parser.add_argument("--breakpoint",
        dest="breakpoint",
        action="store_true",
        help="breakpoint() after operation"
    )
    naive_subparser = naive_parser.add_subparsers(dest="naive_command", required=True)


    # Load the entrypoints
    load_entrypoint_plugins("naive_command")

    # Load plugins
    for registrar in get_commands():
        registrar(naive_subparser)

# def run(args):
#     print("Running safetensors_parser command")