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
    safetensors_parse_parser.add_argument('--device', type=int, default="cpu")
    safetensors_parse_parser.add_argument("path")
    safetensors_parse_parser.set_defaults(func=safetensors_parse)


    safetensors_parse_parser = safetensors_subparser.add_parser(
        "index", help="parse sharded safetensors with json and safetensors libraries"
    )
    safetensors_parse_parser.add_argument("--framework", default="numpy")
    safetensors_parse_parser.add_argument('--device', type=int, default="cpu")
    safetensors_parse_parser.add_argument("path")
    safetensors_parse_parser.set_defaults(func=safetensors_parse)


# yannt naive --breakpoint safetensors parse ./models/bert/test.safetensors
def safetensors_parse(args):
    import os
    import json
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


def safetensors_parse_index(args):
    import os
    import json
    import safetensors
    import safetensors.numpy

    model_dir = os.path.dirname(args.path)
    with open(args.path) as f:
        index = json.load(f)
    weight_map = index["weight_map"]

    shard_tensors = {}
    for tensor_name, shard_file in weight_map.items():
        shard_tensors.setdefault(shard_file, []).append(tensor_name)
    
    shard_metadata = {}
    tensors = {}
    for shard_file, names in shard_tensors.items():
        shard_path = os.path.join(model_dir, shard_file)
        with safetensors.safe_open(shard_path, framework=args.framework, device=args.device) as f:
            shard_metadata[shard_file] = f.metadata()
            for name in names:
                tensors[name] = f.get_tensor(name)

    if args.breakpoint:
        print(f"Locals: {list(locals().keys())}")
        print(f"Example: tensors[list(tensors.keys())[0]]")
        print(f"Example: tensors.keys()")
        print(f"Example: tensors.get_tensor(tensors.keys()[0])")
        print(f"Example: shard_metadata[shard_metadata.keys()[0]]")
        breakpoint()

    


# TODO: Support non-numpy frameworks: pt, tf, flax



# import json
# import os
# from safetensors import safe_open

# model_dir = "model"

# # Step 1: load index
# with open(os.path.join(model_dir, "model.safetensors.index.json")) as f:
#     index = json.load(f)

# weight_map = index["weight_map"]

# # Step 2: group tensors by shard
# shard_to_tensors = {}

# for tensor_name, shard_file in weight_map.items():
#     shard_to_tensors.setdefault(shard_file, []).append(tensor_name)

# # Step 3–4: open shards and read tensors
# tensors = {}

# for shard_file, names in shard_to_tensors.items():
#     shard_path = os.path.join(model_dir, shard_file)

#     with safe_open(shard_path, framework="numpy") as f:
#         for name in names:
#             tensors[name] = f.get_tensor(name)

# print("Loaded tensors:", len(tensors))