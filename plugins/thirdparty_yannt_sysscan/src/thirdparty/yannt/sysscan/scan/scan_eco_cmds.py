#!/usr/bin/env python3

import os
import shutil

from meta import common_cmds

# Home folders to consider:
#   "~/.local/bin"
#   "~/.cargo/bin"
#   "~/.npm/bin"
#   "~/.pyenv/shims"
#   "~/.local/share/flatpak/exports/bin"
# Versioned Folders:
# /usr/lib/nvidia-*/bin
# $ANDROID_HOME
# /opt/intel/oneapi/*/lib

orig_path = os.environ.get("PATH")
wide_posix_path = [
    orig_path,
    "/usr/local/sbin",
    "/usr/local/bin",
    "/usr/sbin",
    "/usr/bin",
    "/sbin",
    "/bin",
    "/usr/local/games",
    "/usr/games",
    "/opt/bin",
    "/opt/local/bin",
    "/opt/nvidia/bin",
    "/opt/homebrew/bin",
    "/snap/bin",
    "/var/lib/flatpak/exports/bin",
    "/nix/var/nix/profiles/default/bin",
    "/opt/rocm/bin",
    "/opt/rocm/llvm/bin",
    "/opt/rocm/profiler/bin",
    "/opt/intel/oneapi/compiler/latest/bin",
    "/opt/intel/oneapi/dpcpp/latest/bin",
    "/opt/intel/oneapi/vtune/latest/bin",
    "/opt/intel/oneapi/advisor/latest/bin",
    "/usr/local/Ascend/bin",
    "/usr/local/Ascend/ascend-toolkit/latest/bin",
    "/opt/ascend/bin",
    "/opt/kunlun/bin",
    "/opt/baidu/xpu/bin",
    "/opt/paddle/bin",
    "/opt/cambricon/bin",
    "/opt/neuware/bin",
    "/opt/biren/bin",
    "/opt/brt/bin",
    "/opt/musa/bin",
]

# Library paths:
# "/opt/alibaba/lib",
# "/opt/hanguang/lib",
# "/opt/kunlun/lib",
# "/opt/baidu/xpu/lib",

os.environ["PATH"] = ':'.join(wide_posix_path)

for cmd in common_cmds:
    cmd_path = shutil.which(cmd)
    if cmd_path:
        print(f"Found Command: {cmd_path}")

# suppose /tmp/mycmd exists and is executable
