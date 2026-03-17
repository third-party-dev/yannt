#!/usr/bin/env python3

import os
from meta import common_cmds, common_libs

from thirdparty.yannt.sysscan.scan import find_files


def is_sus_lib(fpath):
    for lib in common_libs:
        if lib.lower() in fpath.lower():
            return True
    return False

def is_sus_cmd(fpath):
    for cmd in common_cmds:
        if fpath.lower().endswith(cmd.lower()):
            return True
    return False

def is_pytorch(fpath):
    if fpath.lower().endswith("site-packages/torch/__init__.py"):
        return True

def is_pytorch_hub(fpath):
    if fpath.lower().endswith(".cache/torch/hub"):
        return True

def is_huggingface(fpath):
    if fpath.lower().endswith(".cache/huggingface"):
        return True


count = 0
found_libs = []
found_cmds = []
found_pytorch = []
found_pytorch_hub = []
found_huggingface = []
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
    if os.path.isfile(fpath) and is_pytorch(fpath):
        found_pytorch.append(fpath)
        print(f"PyTorch: {fpath}")
        continue
    if os.path.isdir(fpath)
        if is_pytorch_hub(fpath):
            found_pytorch_hub.append(fpath)
            print(f"PyTorch Hub Cache: {fpath}")
            continue
        if is_huggingface(fpath):
            found_huggingface.append(fpath)
            print(f"Huggingface Cache: {fpath}")
            continue
    if os.access(fpath, os.X_OK) and os.path.isfile(fpath) and is_sus_cmd(fpath):
        found_cmds.append(fpath)
        print(f"Sus Command: {fpath}")
        continue
    # TODO: Generate list of folder keywords
    # if os.path.isdir(fpath)
    #     found_dirs.append(fpath)
