

def register_naive_mnn(subparsers):
    mnn_parser = subparsers.add_parser("mnn", help="naive mnn command")
    mnn_subparser = mnn_parser.add_subparsers(dest="mnn_command", required=True)
    
    mnn_load_parser = mnn_subparser.add_parser(
        "load", help="load mnn with mnn library"
    )
    #mnn_load_parser.add_argument("--map_location", default="cpu")
    #mnn_load_parser.add_argument("--weights_only", action="store_true", default=False)
    mnn_load_parser.add_argument("path")
    mnn_load_parser.set_defaults(func=mnn_load)


# ! untested
# yannt naive --breakpoint mnn load ./models/yolo/yolov5su.mnn
def mnn_load(args):
    '''
    When importing MNN, you may receive an exception like the following:

      ImportError: /work/cache/venv/yannt-py3.9-podman/lib/python3.9/site-packages/_mn
      ncengine.cpython-39-x86_64-linux-gnu.so: cannot enable executable stack as share
      d object requires: Invalid argument

    On newer kernels, executable stacks are strictly forbidden. To test MNN,
    which requires an executable stack, you need to test in a VM with its
    own kernel when you use a modern kernel.

    Its also worth mentioning that because this is coming from the kernel and
    possibly a container runtime, it is not something that can be overridden inside
    a container or libc. We could _maybe_ do a KVM config? Need a baseline image 
    source before I can consider going down the adhoc VM path.
    '''

    import MNN

    obj = MNN.Interpreter(args.path)
    sess = interpreter.createSession()

    if args.breakpoint:
        print(f"Locals: {list(locals().keys())}")
        print(f"Example: obj.getSessionInput(sess).getShape()")
        print(f"Example: obj.getSessionInput(sess).getDataType()")
        print(f"Example: obj.getSessionOutputAll(sess).items()")
        breakpoint()




