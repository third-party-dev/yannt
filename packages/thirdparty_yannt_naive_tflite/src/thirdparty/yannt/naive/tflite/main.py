

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


# yannt naive --breakpoint tflite load ./models/yolo/yolov5su.pt
def tflite_load(args):
    import tflite
    import flatbuffers

    with open(args.path, "rb") as f:
        buf = f.read()

    model = tflite.Model.GetRootAsModel(buf, 0)

    if args.breakpoint:
        print(f"Locals: {list(locals().keys())}")
        print(f"Example: model.Version()")
        print(f"Example: model.Subgraphs(0)")
        print(f"Example: model.Subgraphs(0).TensorsLength()")
        print(f"Example: model.Subgraphs(0).OperatorsLength()")
        breakpoint()




