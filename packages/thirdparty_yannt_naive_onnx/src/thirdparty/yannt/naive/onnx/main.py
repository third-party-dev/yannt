

def register_naive_onnx(subparsers):
    onnx_parser = subparsers.add_parser("onnx", help="naive onnx command")
    onnx_subparser = onnx_parser.add_subparsers(dest="onnx_command", required=True)
    
    onnx_load_parser = onnx_subparser.add_parser(
        "load", help="load onnx with onnx library"
    )
    #onnx_load_parser.add_argument("--map_location", default="cpu")
    #onnx_load_parser.add_argument("--weights_only", action="store_true", default=False)
    onnx_load_parser.add_argument("path")
    onnx_load_parser.set_defaults(func=onnx_load)


# TODO: Can we auto-detect missing modules after unpickle fails?
# pip install ultralytics
# apt-get install libgl1
# yannt naive --breakpoint onnx load ./models/yolo/yolov5su.pt
def onnx_load(args):
    import onnx

    model = onnx.load(args.path)

    if args.breakpoint:
        print(f"Locals: {list(locals().keys())}")
        print(f"Example: model.graph")
        print(f"Example: model.graph.input[0].type.tensor_type.shape.dim")
        print(f"Example: model.graph.initializer[0]")
        print(f"Example: onnx.checker.check_model(model)")
        print(f"Example: print(onnx.helper.printable_graph(model.graph))")
        breakpoint()




