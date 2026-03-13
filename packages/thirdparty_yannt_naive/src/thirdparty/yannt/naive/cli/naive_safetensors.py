import traceback
from pprint import pprint


def register_naive_safetensors(subparsers):
    safetensors_parser = subparsers.add_parser(
        "safetensors", help="safetensors command"
    )
    safetensors_subparser = safetensors_parser.add_subparsers(
        dest="safetensors_command", required=True
    )
    
    safetensors_parse_parser = safetensors_subparser.add_parser(
        "parse", help="parse safetensors with safetensors library"
    )
    safetensors_parse_parser.add_argument("--framework", default="numpy")
    safetensors_parse_parser.add_argument('--device', type=int, default=None)
    safetensors_parse_parser.add_argument("path")
    safetensors_parse_parser.set_defaults(func=safetensors_parse)


# yannt naive --breakpoint safetensors parse ./models/bert/test.safetensors
def safetensors_parse(args):
    import safetensors
    import safetensors.numpy
    tensors = safetensors.numpy.load_file(args.path)
    safe_obj = safetensors.safe_open(args.path, framework=args.framework, device=args.device)

    if args.breakpoint:
        print(f"Locals: {list(locals().keys())}")
        print(f"Example: tensors[list(tensors.keys())[0]]")
        print(f"Example: safe_obj.keys()")
        print(f"Example: safe_obj.get_tensor(safe_obj.keys()[0])")
        print(f"Example: safe_obj.metadata()")
        breakpoint()


# TODO: Support non-numpy frameworks: pt, tf, flax