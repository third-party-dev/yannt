# AMD

## Hardware

Any system information pertaining to AI

Kernel driver in use: vfio-pci    -> using VM

lsmod | grep amdgpu
lsmod | grep amdkfd

ls /sys/class/drm/
cat /sys/class/drm/card0/device/vendor
- 0x10de → NVIDIA
- 0x1002 → AMD
- 0x8086 → Intel

dmesg | grep -i iommu

ls /dev/dri/renderD*

```

```python
from pathlib import Path

for p in Path("/sys/class/drm").glob("card*/device/vendor"):
    print(p.read_text().strip())
```

## Drivers

The things that driver hardware.

- /lib/modules/*/kernel/drivers/gpu/drm/amd/amdgpu/
  - amdgpu.ko
  - amdkfd.ko
  - radeonsi_dri.so	OpenGL
  - libEGL_mesa.so	
  - libGLX_mesa.so	
  - libvulkan_radeon.so	
  - libLLVM*.so
- Paths:
  - /usr/lib/x86_64-linux-gnu/dri/
  - /usr/lib/x86_64-linux-gnu/

- OpenCL
  - libOpenCL.so
  - libMesaOpenCL.so
  - libRusticlOpenCL.so
  - /etc/OpenCL/vendors/mesa.icd
- ROCm Stack
  - libhsa-runtime64.so
  - libamdhip64.so
  - librocclr.so
  - libhsakmt.so
- HIP
  - libamdhip64.so
  - libhiprtc.so
  - libhsa-runtime64.so
  - libamdhip64.so
  - hipcc
- ML Libs
  - librocblas.so
  - libhipblas.so
  - libhipsparse.so
  - librocsolver.so
  - libMIOpen.so (cuDNN equivalent)
  - librocfft.so
  - libhiprand.so
- Profiling Tracing
  - libroctracer64.so
  - librocprofiler64.so
- AMGGPU Pro
  - libamdocl64.so (OpenCL)
  - libdrm_amdgpu.so
  - libvulkan_amdgpu.so
  - /etc/OpenCL/vendors/amdocl64.icd

- ELF Inspection
- readelf -d binary | grep NEEDED
  - libhsa-runtime64.so
  - libamdhip64.so
  - librocblas.so
  - libMIOpen.so
  - libamdocl64.so
- nm -D binary | grep -E "(hip|hsa|roc)"
- strings binary | grep -E "amdgcn|gfx[0-9]+"
- readelf -S binary | grep -E "hsaco|amdgpu|hip"
- strings binary | grep "\.hsaco"

- Ambguity
  - libOpenCL.so
  - libMesaOpenCL.so 

- lib(hsa|hip|roc|amdocl|amdgpu).*\.so
- readelf -d | grep -E "libhsa-runtime|libamdhip64"
- nm -D | grep -E "hip|hsa_|roc"
- strings | grep gfx[0-9]
