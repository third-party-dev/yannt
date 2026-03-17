def register_naive_pytorch(subparsers):
    pytorch_parser = subparsers.add_parser("pytorch", help="naive pytorch command")
    pytorch_subparser = pytorch_parser.add_subparsers(dest="pytorch_command", required=True)
    
    pytorch_load_parser = pytorch_subparser.add_parser(
        "load", help="load pytorch with pytorch library"
    )
    pytorch_load_parser.add_argument("--map_location", default="cpu")
    # TODO: Consider controlling weights_only
    pytorch_load_parser.add_argument("--weights_only", action="store_true", default=False)
    pytorch_load_parser.add_argument("path")
    pytorch_load_parser.set_defaults(func=pytorch_load)

    # TODO: User needs to specify the model imports
    # pytorch_load_params_parser = safetensors_subparser.add_parser(
    #     "load_params", help="load pytorch params with pytorch library"
    # )
    # pytorch_load_params_parser.add_argument("--map_location", default="cpu")
    # pytorch_load_params_parser.add_argument("path")
    # pytorch_load_params_parser.set_defaults(func=pytorch_load_params)

# TODO: Can we auto-detect missing modules after unpickle fails?
# pip install ultralytics
# apt-get install libgl1
# yannt naive --breakpoint pytorch load ./models/yolo/yolov5su.pt
def pytorch_load(args):
    import torch
    
    # TODO: Consider running yannt safety checks on pickle.

    model = torch.load(args.path, map_location=args.map_location, weights_only=args.weights_only)

    if args.breakpoint:
        print(f"Locals: {list(locals().keys())}")
        print(f"Example: type(model)")
        print(f"  Note: torch.nn.Module - full model")
        print(f"  Note: dict - checkpoint")
        print(f"  Note: OrderedDict - state_dict")
        print(f"state_dict Example:")
        print(f"  for k, v in sd.items():")
        print(f"      print(k, v.shape, v.dtype)")
        print(f"checkpoint Example: model['model'].state_dict()")
        breakpoint()


# TODO: User needs to specify the model imports
# def pytorch_load_params(args):
#     import torch
#     from mymodel import MyModel

#     model = MyModel()
#     state_dict = torch.load("weights.pt", map_location="cpu")
#     model.load_state_dict(state_dict)

