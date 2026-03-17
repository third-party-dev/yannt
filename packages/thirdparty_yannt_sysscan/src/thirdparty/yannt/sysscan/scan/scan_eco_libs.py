#!/usr/bin/env python3

import os
import struct

from meta import common_libs

# unused atm
common_lib_paths = [
    # --- Nvidia ---
    "/usr/local/cuda/lib64",
    "/usr/local/cuda/lib",
    "/opt/cuda/lib64",
    "/opt/cuda/lib",
    "/opt/nvidia/lib",
    "/opt/nvidia/lib64",
    # --- AMD ---
    "/opt/rocm/lib",
    "/opt/rocm/lib64",
    # --- Intel ---
    "/opt/intel/oneapi/compiler/latest/lib",
    "/opt/intel/oneapi/mkl/latest/lib",
    "/opt/intel/oneapi/mkl/latest/lib/intel64",
    "/opt/intel/oneapi/runtime/latest/lib",
    "/opt/intel/oneapi/compiler/latest/lib/intel64",
    "/opt/intel/openvino/lib",
    "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64",
    "/opt/intel/oneapi/level-zero/latest/lib",
    "/opt/intel/oneapi/sycl/latest/lib",
    # --- Alibaba ---
    "/opt/alibaba/lib",
    "/opt/hanguang/lib",
    # --- Baidu ---
    "/opt/kunlun/lib",
    "/opt/baidu/xpu/lib",
    # --- Cambricon ---
    "/opt/cambricon/lib",
    "/opt/neuware/lib",
    # --- Biren ---
    "/opt/biren/lib",
    "/opt/brt/lib",
    # --- Moore Threads ---
    "/opt/musa/lib",
    # --- Common ---
    "/usr/lib",
    "/usr/lib64",
    "/usr/lib/x86_64-linux-gnu",
]

def is_printable_ascii(byt):
    return 32 <= byt and byt < 127

def read_ldcache(path="/etc/ld.so.cache"):
    libs = []
    with open(path, "rb") as f:
        # Scan for ASCII strings ending with ".so"
        data = f.read()
        current = []
        for byt in data:
            if is_printable_ascii(byt):
                current.append(chr(byt))
            else:
                if len(current) > 0:
                    s = ''.join(current)
                    if s.endswith(".so"):
                        libs.append(s)
                    current = []
    return libs

def get_sus_ldcache_libs():
    # - Enties are like: "libOpenCL.so.1 (libc6,x86-64) => /lib/x86_64-linux-gnu/libOpenCL.so.1"
    #   therefore we can't use endswith.
    found_ml_libs = {}
    for lib in read_ldcache():
        llib = lib.lower()
        for clib in common_libs:
            lclib = clib.lower()
            if lclib in llib:
                if clib not in found_ml_libs:
                    found_ml_libs[clib] = [lib]
                else:
                    found_ml_libs[clib].append(lib)
    return found_ml_libs

found_ml_libs = get_sus_ldcache_libs()
print(f"Found {len(found_ml_libs)} libraries in ld.so.cache.")
for ml_lib in found_ml_libs:
    print(f"Library: {found_ml_libs[ml_lib]}")
