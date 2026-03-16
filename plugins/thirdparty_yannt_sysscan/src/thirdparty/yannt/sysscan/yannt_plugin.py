
def register_yannt_sysscan(subparsers):
    sysscan_parser = subparsers.add_parser(
        "sysscan", help="sysscan command"
    )
    sysscan_parser.add_argument("--breakpoint", dest="breakpoint", action="store_true", default=False)

    sysscan_subparser = sysscan_parser.add_subparsers(
        dest="transformers_command", required=True
    )

    sysscan_full_parser = sysscan_subparser.add_parser("full", help="full sysscan command")
    sysscan_full_parser.set_defaults(func=full_sysscan)

    sysscan_quick_parser = sysscan_subparser.add_parser("quick", help="quick sysscan command")
    sysscan_quick_parser.set_defaults(func=quick_sysscan)


def full_sysscan(args):
    import os
    # Initialize the artifact metadata.
    from thirdparty.yannt.sysscan.meta import init_database, DB
    init_database(DB)

    from thirdparty.yannt.sysscan.scan import find_files

    sus_cmds = DB._get_cmds()
    def is_sus_cmd(fpath):
        for cmd in sus_cmds:
            if fpath.lower().endswith(cmd.lower()):
                return True
        return False

    sus_libs = DB._get_libs()
    def is_sus_lib(fpath):
        for lib in sus_libs:
            if lib.lower() in fpath.lower():
                return True
        return False

    sus_relpaths = DB._get_relpaths()
    def is_sus_relpath(fpath):
        for relpath in sus_relpaths:
            if fpath.lower().endswith(relpath.lower()):
                return True
        return False

    count = 0
    found_libs = []
    found_cmds = []
    found_relpath = []
    for fpath in find_files("/"):
        count += 1
        if count % 1000000 == 0:
            print(f"Processed {count} files.")
        if fpath.startswith(("/sys", "/proc", "/dev")):
            continue
        # Quick library filter
        if ".so" in fpath and is_sus_lib(fpath):
            found_libs.append(fpath)
            print(f"Sus Library: {fpath}")
            continue
        # if os.path.isfile(fpath) and is_pytorch(fpath):
        #     found_pytorch.append(fpath)
        #     print(f"PyTorch: {fpath}")
        #     continue
        if os.path.isdir(fpath) and is_sus_relpath(fpath):
            found_relpath.append(fpath)
            print(f"Sus Relpath: {fpath}")
            continue
        if os.access(fpath, os.X_OK) and os.path.isfile(fpath) and is_sus_cmd(fpath):
            found_cmds.append(fpath)
            print(f"Sus Command: {fpath}")
            continue
        # TODO: Generate list of folder keywords
        # if os.path.isdir(fpath)
        #     found_dirs.append(fpath)
    print("Done full scan.")

def quick_sysscan(args):
    # Initialize the artifact metadata.
    from thirdparty.yannt.sysscan.meta import init_database, DB
    init_database(DB)

    from thirdparty.yannt.sysscan.scan.kernel import \
        scan_gpus, read_loaded_modules, sus_gpu_driver, kernel_taint_flags

    # lspci | grep GPUID
    gpus = scan_gpus()
    if not gpus:
        print("No GPU devices found.")
        return
    print(f"Found {len(gpus)} GPU(s):\n")
    for gpu in gpus:
        print(f"PCI Address : {gpu['pci_address']}")
        print(f"Vendor      : {gpu['vendor']} ({gpu['vendor_id']})")
        print(f"Device      : {gpu['device']} ({gpu['device_id']})")
        print(f"Class       : 0x{gpu['class']}")
        print(f"Driver      : {gpu['kernel_driver']}")
        print("-" * 60)

    # lsmod | grep PREFIX
    modules = read_loaded_modules()
    gpu_modules = [mod for mod in modules if sus_gpu_driver(mod['name'])]
    print(f"Found {len(gpu_modules)} GPU (or VM) Drivers(s):\n")
    for module in gpu_modules:
        print(f"Name  : {module['name']}")
        print(f"Size  : {module['size']}")
        print(f"Refs  : {module['refcount']}")
        # TODO: Check deps for "common" modules?
        print(f"Deps  : {module['deps']}")
        print(f"State : {module['state']}")
        print("-" * 60)

    # cat /proc/sys/kernel/tainted
    print(f"Kernel taint flags: {kernel_taint_flags() or 'none'}")


    print("Done quick scan.")
