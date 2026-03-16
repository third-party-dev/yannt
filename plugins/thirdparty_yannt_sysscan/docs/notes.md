# Scanner

## Hardware

Scanning relavant hardware specifications. This is qureied via the kernel. Indicators include:

- Kernel ring long (dmesg) (not impl)
- Kernel loaded modules (/proc/modules)
  - Based on kernel object prefixes
  - Based on kernel object dependencies (not impl) 
- Kernel unloaded modules (not impl)
- Kernel PCI listings

## Ecosystem Libraries and Tools

The idea with this is that we want to find common libraries or commands associated with various ecosystems. 

- What is in $PATH? ... we come with our own PATH too.
  - Common command names
- What is in `ldconfig -p`? ... index of whats available.
  - This will miss dlopen-ed things.
- What is resolvable by ctypes? `ctypes.util.find_library(lib)` (not impl)
- What is installed with package management?
  - dpkg `dpkg -l | grep -E "nvidia|cuda|cudnn|libcublas"` (not impl)
  - rpm `rpm -qa | grep -E "nvidia|cuda"` (not impl)
- Scan the whole file system for:
  - common libs and common commands.
  - Pattern matching (not impl)
- Scan the whole file system and look for "keywords" in path. (not impl)
  - common keywords 
  - Pattern matching (not impl)
- Scan all ELF objects for indicators:
  - Symbol search (`nm -D libfoo.so | grep -E "cuInit|cuLaunch|cudaMalloc"`) (not impl)
  - Section search (`readelf -S libfoo.so | grep -E "nv_fatbin|.nvFatBinSegment"`) (not impl)
  - String search (`strings libfoo.so | grep -E "\.ptx|sm_[0-9]+"`) (not impl)
    - .nv_fatbin, .nvFatBinSegment, .nv.info
  - Note search (`readelf -n libfoo.so`)
    - NVIDIA, CUDA, NVVM
  - Dependency Searching
  
## General Libraries and Platforms

- PyTorch / Torch
  - Libraries and Drivers
  - Hub Cache 
- Tensorflow
- Onnx
- Huggingface
  - transformers
  - cache

## Agents

- AutoGPT
- Goose

## Model Runtimes

- LMStudio
  - Assets (e.g. Models)
- Ollama
  - Assets (e.g. Models)

## Models

- PyTorch
- Onnx
- Gguf
- Tflite
- Tensorflow
