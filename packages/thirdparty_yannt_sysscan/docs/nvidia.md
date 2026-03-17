# Nvidia

Any system information pertaining to AI

```
lspci | grep -i nvidia
lsmod | grep nvidia
nvidia-smi
```

```python
  import ctypes.util
  
  for lib in ["cuda", "cudart", "cublas", "cudnn"]:
      print(lib, "→", ctypes.util.find_library(lib))
      
  import ctypes
  ctypes.CDLL("libcuda.so.1")
  print("CUDA driver loaded")
```

- Look at library dependencies for common cuda drivers:
  - libcuda.so.1
  - libnvidia-ml.so.1
  - libcudart.so.*
  - libnvrtc.so
  - libnvidia-fatbinaryloader.so
  - `nm -D libfoo.so | grep -E "cuInit|cuLaunch|cudaMalloc"`
  - `readelf -S libfoo.so | grep -E "nv_fatbin|.nvFatBinSegment"`
  - `strings libfoo.so | grep -E "\.ptx|sm_[0-9]+"`
    - .nv_fatbin
    - .nvFatBinSegment
    - .nv.info
  - `readelf -n libfoo.so`
    - NVIDIA
    - CUDA
    - NVVM
- Patterns
  - libcu*.so
  - libnv*.so
  - libnvidia-*.so
  - NOT: libnvidia-ml.so
  - NOT: libnvrtc.so
