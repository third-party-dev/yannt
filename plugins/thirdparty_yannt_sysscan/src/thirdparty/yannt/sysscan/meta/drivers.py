
def init_driver_entries(db):
    # Drivers / Hardware
    db.add(name="nvidia_drv", member_of=["drivers"],
        cmds=[
            "nvidia-smi", "nvidia-debugdump", "nvidia-modprobe", "nvidia-persistenced",
            "nvidia-settings", "nvidia-xconfig",
            "nvidia-ml-py", # NV Management Library (NVML)
        ],
    )
    db.add(name="amdgpu_drv", member_of=["drivers"], cmds=["amd-smi",],)
    db.add(name="huawei_npu", member_of=["drivers"], cmds=["npu-smi", "torch_npu"], libs=["libtorch_npu.so",],)

    # Container Runtimes
    db.add(name="nvidia_cri", cmds=["nvidia-container-cli", "nvidia-container-runtime",], member_of=["crt"],)
    db.add(name="amd_rocm_cri", cmds=["rocm-container-runtime",], member_of=["crt"],)
    db.add(name="alibaba_cri", cmds=["ali-container-runtime",], member_of=["crt"],)
