## --- Container ---

### zip

- Magic Bytes: `50 4B 03 04` or `PK\x03\x04`
  - Empty Archive is `50 4B 05 06` or `PK\x05\x06`.
  - Split Archive is `50 4B 07 08` or `PK\x07\x08`.


## --- Serialization ---

### flatbuffers

- schema based
  - can deduce many fields (not types) based on offsets

### json

- printable

### xml

- printable

### pickle

- ISA

### protobuf

- binary
- schema based

- is protobuf if wire protocol valid up to X bytes

## --- Model ---

### gguf

- proprietary format
- Background: ggml / llama.cpp community.
- Comp Graph? No (graph in runtime)

- Magic Bytes: `GGUF` or `47 47 55 46`
- Portable Runtime

## om

- Magic Bytes: `IMOD` or `49 4d 4f 44`
- Proprietary Container Format

## onnx

- Interchange Format (.onnx)

- pure protobuf
- openly available schema
- Comp Graph? Yes

- Usual ModelProto Start:
  - `00`: `08 <ir_version>`
  - `02`: `12 <producer_name_length> <producer_name_string>`
  - `02+2+<producer_name_length>`: `1a <producer_version_length> <producer_version_string>`
  - `02+2+<producer_name_length>+<producer_version_length>`: `3a <LEN-value>`
    - bit7 - 0 - continuation bit
    - bit6-3 - 0111 - field number (=7)
    - bit2-0 - 010 - length type field
    - LEN-value's first byte's first bit (high bit) should be 1 (and also the next one) or the GraphProto is likely too small.
  
- Magic Bytes:
  - `08 ?? 12`
  - Contains `3a` (aligned on 32 bit boundary) + (at least) next 2 bytes high bit set within first 64 bytes.
  - _likely_ contains the word `model`

### pytorch

- Interchange Format: TorchScript (.pt), PyTorch ExportedProgram (.pt2)

- extensions: .pt, .pth, .bin (usually contains state_dict i.e. list of tensors)
  - pytorch lightening / torch.save: .ckpt (contains optimizer, scheduler, and trainer state)
- zip
- observed `data.pkl` as always first zip entry
- Comp Graph? Yes (sometimes)
- Training Format? Yes
- Magic Bytes:
  - Because `data.pkl` is always first, if we're not looking at a split archive, offset 30 (of the ZIP) should always be `data.pkl`.

- UNVERIFIED: pickle bytes `80 02 8a 0a 6c fc 9c 46 f9 20 6a a8 50 19 2e`
- UNVERIFIED ExecuTorch: `45 54 31 32`

### safetensors

- layout:
  - 64bit length of header
  - JSON header
  - Tensor Data (defined by JSON header)
- Comp Graph? No

- Magic Bytes:
  - Offset 6-7: `00 00`
  - Offset 8-9: `{"`
  - Contains: `"__metadata__"`
  - Contains: `"dtype"` followed by `:"F32"` or any other STTYPE.
  - Contains: `"shape"`
  - Contains: `"data_offsets"`

- GPTQ, AWQ, and EXL2 models are stored as safetensors.

## mnn

- Portable Runtime
- files: *.mnn

- Pure Flatbuffers
- Magic Bytes:
  - root_offset - offset 0 (u32) - must be 4 byte aligned.
  - vtbl_rel_off - first 4 bytes of root offset (i32)
  - vtbl_abs_off = root_offset - vtbl_rel_off (first 4 of root_tbl)
  - vtbl_size (in bytes) is (u16) at vtbl_abs_off
  - vtbl_size must be >= 20 to support MNN's Net object's slot 7 "tensorName" (vtbl byte 18)
  - offset 4-7 must not be TFL3

### tflite3

- pure flatbuffers
- openly available schema
- Comp Graph? Yes
- Target Specific?
- Magic Bytes:
  - Offset 0: Root Table Offset
  - Offset 4: `TFL3`

- Portable Runtime
- files: .tflite

- Target Specific Runtime
- files: *_edgetpu.tflite (magic: `54 46 4c 33`)

- UNVERIFIED checkpoint index: `57 fb 80 8b 24 75 47 db`
- UNVERIFIED LiteRT: `54 46 4c 33`

## --- Unverified ---

### TensorRT

- Target Specific Runtime
- files: *.engine, *.plan

### RKNN

- Target Specific Runtime
- files: *.rknn
- UNVERIFIED `52 4b 4e 4e`

### Hailo

- Target Specific Runtime
- files: *.her

### Qualcomm QNN

- Target Specific Runtime
- files: *.bin

### Qualcomm SNPE

- Target Specific Runtime
- files: *.dlc
- UNVERIFIED `50 4b 03 04`
- ZIP?

### Core ML compiled

- Target Specific Runtime
- files: *.mlmodelc

### OpenVINO compiled

- Target Specific Runtime
- files: *.blob

### AWS Neuron

- Target Specific Runtime
- files: *.neff

### MediaTek NeuroPilot

- Target Specific Runtime
- files: *.dla

### VeriSilicon NPU

- Target Specific Runtime
- files: *.nb
- UNVERIFIED: `56 50 4d 4e`

### Sophgo / Cvitek

- Target Specific Runtime
- files: *.bmodel, *.cvimodel
- UNVERIFIED sophgo: `ee aa 55 ff`
- UNVERIFIED cvitek: `43 76 69 4d 6f 64 65 6c`

### Kneron

- Target Specific Runtime
- files: *nef


### TVM / AOTInductor

- Target Specific Runtime
- files: *.so,*.dylib,*.dll + params

### OpenVINO

- Portable Runtime
- files: *.xml (graph), *.bin (weights)

### Core ML

- Portable Runtime
- files: *.mlmodel (protobuf), .mlpackage/{Manifest.json, weight files}

### ExecuTorch

- Portable Runtime
- files: *.pte (flatbuffers)
- can support more backends: XNNPACK, Core ML, QNN, or Vulkan

### NNEF

files: graph.nnef, *.dat (magic: `4e ef`)

### TNN

- Portable Runtime
- files: *.tnnproto, *.tnnmodel
- UNVERIFIED tnnmodel: `02 00 bc fa`

### NCNN

- Portable Runtime
- files: *.param + *.bin
- UNVERIFIED param: `37 37 36 37 35 31 37`
- UNVERIFIED param.bin: `dd 85 76 00`

### Onnx Runtime

- Portable Runtime
- files: .ort
- Magic Bytes: ORTM

- UNVERIFIED `4f 52 54 4d`


### StableHLO

- Interchange Format
- files: *.mlirbc
- UNVERIFIED: `4d 4c ef 52 `

### Paddle Inference

- Interchange Format
- files: .pdmodel + .pdiparams

### Tensorflow

- Training Framework Format
- Interchange Format: SavedModel (saved_model.pb), TF frozen graph (*.pb)

- extensions: .index + .data-NNNNN-of-NNNNN
- protobuf + shards
- Comp Graph? ???

### Keras v3

- Training Framework Format
- files: config.json, metadata.json, model.weights.h5
- ZIP

### Keras Legacy

- Training Framework Format
- files: *.h5
- Serialization: HDF5
- UNVERIFIED Magic Bytes: `89 48 44 46 0D 0A 1A 0A`

### JAX/Flax

- Training Framework Format
- files: *.msgpack

### PaddlePaddle

- Training Framework Format
- files: *.pdparams, *.pdopt
- Serialization: Pickle

- UNVERIFIED params: `80 02` - `80 05`

### MXNet

- Training Framework Format
- files: *.params, -symbol.json

- UNVERIFIED params: `12 01 00 00 00 00 00 00`

### Caffe

- Training Framework Format
- files: *.caffemodel, *.prototxt

### Darknet

- Training Framework Format
- files: *.weights, *.cfg

### Numpy

- Training Framework Format
- files: *.npz
- ZIP
- 
- UNVERIFIED array: `93 4e 55 4d 50 59`

### scikit-learn

- Training Framework Format
- files: *.pkl, *.joblib

- UNVERIFIED pickle: `80 0N`

### MindSpore

- ONNX like
- files: .mindir, mind_ir.proto (protobuf)

- AIR (Ascend): *.air
- Lite: *.ms (magic: `4d 53 4c 32`)