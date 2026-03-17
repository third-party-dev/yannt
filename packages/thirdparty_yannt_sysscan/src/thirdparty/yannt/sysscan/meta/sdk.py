
def init_sdk_entries(db):
    # SDKs

    db.add(name="cuda_toolkit", member_of=["sdk"],
        cmds=[
            "nvidia-cuda-mps-control", "nvcc", "nvprune", "cuda-gdb", "cuda-memcheck",
            "compute-sanitizer",
            "deviceQuery", "bandwidthTest", # CUDA Samples
            "cublasLtMatmul", # cuBLAS
        ],
        libs=[
            "libcuda.so", "libcudart.so", "libcublas.so", "libcufft.so",
            "libcurand.so", "libcusolver.so", "libcusparse.so", "libcudnn.so",
            # Not CUDA, but NVidia
            "libnccl.so", "libnpp.so", "libnvrtc.so", "libnvToolsExt.so", "libnvgraph.so",
        ],
    )

    db.add(name="nvidia_insight", member_of=["sdk"],
        cmds=["nsys", "nv-nsight-cu-cli", "ncu",],
        notes=["Performance analysis tool provided by NVidia"]
    )

    db.add(name="amd_rocm_sdk", member_of=["sdk"],
        cmds=[
            "rocminfo", "hipcc", "amdclang", "amdclang++",
            # "clang-offload-bundler", # Generic, but often used with GPU dev
            "rocprof", "rocscope", "rocgdb", "rocm-smi", "rocm-bandwidth-test",
        ],
        libs=[
            "libhsa-runtime64.so", "libhip_hcc.so", "libamdhip64.so",
            "libhsa.so", "libhcc.so", "librocblas.so", "librocfft.so",
            "librocrand.so", "librocsparse.so", "libmiopen.so", "librccl.so",
        ],
    )

    db.add(name="opencl", member_of=["sdk"],
        cmds=["clinfo"],
        libs=[],
        notes=["Maintained (OSS) by Khronos Group"],
    )

    db.add(name="vulkan", member_of=["sdk"],
        cmds=["vulkaninfo"],
        libs=[],
        notes=["Maintained (OSS) by Khronos Group"],
    )

    db.add(name="intel_gpu", member_of=["sdk"],
        cmds=["intel_gpu_top", "intel_gpu_frequency", "intel_gpu_time", "intel-gpu-tools",],
        libs=[],
    )

    db.add(name="oneapi", member_of=["sdk"],
        cmds=[
            "zeinfo", "ze_tracer", "vtune", "advisor", "icx", "icpx",
            "ifx", "dpcpp", "sycl-ls", "gdb-oneapi",
        ],
        libs=[
            "libsycl.so", "libze_loader.so", "libopencl.so",
            # Not OneAPI, but Intel Math GPU Code
            "libmkl.so", "libmklml.so", "libvpux.so", "libngraph.so", "libtbb.so",
        ],
        notes=["Unified programming model across hardware (by Intel)"]
    )

    db.add(name="openvino", member_of=["sdk"],
        cmds=["benchmark_app", "compile_tool", "ovc",],
        libs=["libinference_engine.so",],
        notes=["Toolkit developed by Intel"],
    )

    db.add(name="habana", member_of=["sdk"],
        cmds=["hl-smi", "habana_container_runtime", "habana_frameworks",],
        libs=[],
        notes=["AI focused Semiconductor company acquired by Intel in 2019"],
    )

    db.add(name="huawei_ascend", member_of=["sdk"],
        cmds=["acl_dump", "aclgraphtool", "ascend-docker-runtime", "npu-container-runtime"],
        libs=["libascendcl.so",],
    )

    db.add(name="hanguang_sdk", member_of=["sdk"],
        cmds=[
            "hanguang-smi", "hgcc", "hg-runtime", "hg-exec", "hgprof", "hgtrace", "onnx-hg-opt",
        ],
        libs=["libhanguang.so", "libhg_runtime.so", "libhg_compiler.so",],
        notes=["Alibaba"],
    )

    db.add(name="pai", member_of=["sdk", "mlops"],
        cmds=["pai-compile", "pai", "pai-job", "pai-run", "pai-container-agent",],
        libs=["libpai_runtime.so",],
        notes=["Maintained by Alibaba"]
    )

    db.add(name="kunlun_sdk", member_of=["sdk"],
        cmds=["kunlun-smi",],
        libs=["libkunlun.so",],
        notes=["Maintained by Alibaba"]
    )

    db.add(name="xpu_sdk", member_of=["sdk"],
        cmds=["xpu-smi", "xpu-info", "xpu-compiler", "xpu-opt",],
        libs=["libxpu.so",
        "libxpu_runtime.so",
        "libxpu_driver.so",],
        notes=["Maintained by Inspur"]
    )

    db.add(name="paddle", member_of=["sdk"],
        cmds=["paddle",],
        libs=["libpaddle_xpu.so",],
        notes=["Maintained (OSS) by Baidu"]
    )

    db.add(name="cambricon_sdk", member_of=["sdk"],
        cmds=["cnmon", "cncc", "cnrt", "cnas",
        "cambricon-container-runtime", "mlu-container-agent",],
        libs=[
            "libcnrt.so", "libmlu.so", "libcnnl.so", "libcncodec.so",
            # Upstream or downstream?
            "libtorch_mlu.so",
        ],
    )

    db.add(name="cambricon_musa", member_of=["sdk"],
        cmds=[
            "musa-smi", "musa-info", "musa-cc", "musa-clang", "musa-opt", "musa-link",
            "musa-runtime", "musa-test", "musaprof", "musatrace", "musa-container-runtime",
        ],
        libs=[
            "libmusa.so", "libmusa_runtime.so",
            # Upstream or downstream?
            "libtorch_musa.so", "libtensorflow_musa.so",
        ],
        notes=["MUSA (Multi-Usage Computing Architecture) is an architecture by Cambricon"]
    )

    db.add(name="biren_sdk", member_of=["sdk"],
        cmds=[
            "biren-smi", "brcc", "brclang", "brclang++", "brtinfo",
            "brtexec", "brt-opt", "brt-compile", "brprof", "brtrace",
        ],
        libs=[
            "libbrt.so", "libbiren.so", "libbiren_gpu.so", "libbrcuda.so",
            # Upstream or downstream?
            "libtorch_biren.so",
        ],
    )
