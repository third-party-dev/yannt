

def register_naive_tflite(subparsers):
    tflite_parser = subparsers.add_parser("tflite", help="naive tflite command")
    tflite_subparser = tflite_parser.add_subparsers(dest="tflite_command", required=True)
    
    tflite_load_parser = tflite_subparser.add_parser(
        "load", help="load tflite with tflite library"
    )
    #tflite_load_parser.add_argument("--map_location", default="cpu")
    #tflite_load_parser.add_argument("--weights_only", action="store_true", default=False)
    tflite_load_parser.add_argument("path")
    tflite_load_parser.set_defaults(func=tflite_load)


# TODO: Can we auto-detect missing modules after unpickle fails?
# pip install ultralytics
# apt-get install libgl1
# yannt naive --breakpoint tflite load ./models/yolo/yolov5su.pt
def tflite_load(args):
    import tflite

    model = tflite.load(args.path)

    if args.breakpoint:
        print(f"Locals: {list(locals().keys())}")
        print(f"Example: model.graph")
        print(f"Example: model.graph.input[0].type.tensor_type.shape.dim")
        print(f"Example: model.graph.initializer[0]")
        print(f"Example: tflite.checker.check_model(model)")
        print(f"Example: print(tflite.helper.printable_graph(model.graph))")
        breakpoint()




