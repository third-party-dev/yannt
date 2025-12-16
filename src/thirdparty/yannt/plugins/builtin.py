from thirdparty.yannt.registry import register_command

def register(subparsers):
    parser = subparsers.add_parser("hello", help="Say hello")
    parser.add_argument("--name", default="world")
    parser.set_defaults(func=run)

def run(args):
    print(f"Hello, {args.name}!")

register_command("hello", register)