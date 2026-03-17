

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

    try:
        import MNN
    except ImportError as e:
        if 'stack' in str(e):
            print('''
------------------------------------------------------------------------------
When importing MNN, you may receive an exception like the following:

```text
ImportError: /work/cache/venv/yannt-py3.9-podman/lib/python3.9/site-packages/
_mnncengine.cpython-39-x86_64-linux-gnu.so: cannot enable executable stack as
 shared object requires: Invalid argument
```

On newer kernels, executable stacks are strictly forbidden. To test MNN,
which requires an executable stack, you need to test in a VM with its
own (older) kernel when you use a modern kernel on the host.

Because this executable stack exception is coming from the kernel and
possibly a container runtime, it is not something that can be overridden
inside a container or libc fix.

We could _maybe_ do a yannt KVM config? But to continue with this, I would 
need to know of a "upstream" VM image source to baseline any VMs on. yannt
is not in the business of generating OS installs from scratch.
------------------------------------------------------------------------------
            ''')
        raise

    obj = MNN.Interpreter(args.path)
    sess = interpreter.createSession()

    if args.breakpoint:
        print(f"Locals: {list(locals().keys())}")
        print(f"Example: obj.getSessionInput(sess).getShape()")
        print(f"Example: obj.getSessionInput(sess).getDataType()")
        print(f"Example: obj.getSessionOutputAll(sess).items()")
        breakpoint()




