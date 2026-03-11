# Ident Use Cases

## List Known Serialized Model Formats

```sh
yannt pparse ident list
```

Output:

```text
acuity - Acuity ML
armnn - Arm NN ML
barracuda - Barracuda ML
bigdl - BigDL ML
caffe - Caffe ML
caffe2 - Caffe2 ML
cambricon - Cambricon (model/accelerator context)
catboost - CatBoost ML
circle - Circle ML
cntk - CNTK (Microsoft Cognitive Toolkit) ML
coreml - Core ML
darknet - Darknet ML
dl4j - DL4J ML
dlc - DLC (DeepLabCut)
dot - DOT (GraphViz / Neural network graph export)
espresso - Espresso (ML/format)
executorch - ExecuTorch
flax - Flax
flux - Flux (Julia)
gguf - GGUF (GGML Unified Format)
hailo - Hailo
hickle - Hickle
kann - KANN
keras - Keras
kmodel - Kendryte / Kendryte K210
lasagne - Lasagne
lightgbm - LightGBM
mediapipe - MediaPipe
megengine - MegEngine
mlir - MLIR
mlnet - ML.NET
mnn - MNN
mslite - MSLite
mxnet - MXNet
ncnn - NCNN
nnabla - NNabla
nnc - NNC (Neural Network Coding / NNC Standard)
nnef - NNEF
numpy - NumPy
om - OM (Huawei MindSpore)
onednn - oneDNN
onnx - ONNX
openvino - OpenVINO
paddle - PaddlePaddle
pickle - Pickle
pytorch - PyTorch
qnn - QNN
rknn - RKNN
safetensors - SafeTensors
sentencepiece - SentencePiece
sklearn - scikit-learn (sklearn)
tengine - Tengine
tensorrt - TensorRT
tf - TensorFlow (TF)
tflite - TensorFlow Lite (TFLite)
tnn - TNN
torch - Torch
transformers - Transformers (Hugging Face)
tvm - TVM
uff - UFF (Universal Framework Format)
vnnmodel - VNN (Verifiable Neural Networks) Challenge/Standard
weka - Weka
xgboost - XGBoost
xmodel - XModel
```

List known types with python:

```python
from thirdparty.pparse.ident.extensions import typedb

for k,val in typedb.items():
    print(f'{k} - {val["name"]}')
```

## Show information about serialized model format

```sh
yannt pparse ident show pytorch
```

Output:

```text
Name: PyTorch
Purpose: Deep learning framework for training and inference.
Maintainer: Meta / PyTorch community.
Links:
- https://pytorch.org
- https://github.com/pytorch/pytorch
Notes:
- Serialization format: .pt / .pth (TorchScript / state_dict).
Extentions: ['.pt', '.pth', '.ptl', '.pt1', '.pt2', '.pyt', '.pyth', '.pkl', '.pickle', '.h5', '.t7', '.model', '.dms', '.tar', '.ckpt', '.chkpt', '.tckpt', '.bin', '.pb', '.zip', '.nn', '.torchmodel', '.torchscript', '.pytorch', '.ot', '.params', '.trt', '.ff', '.ptmf', '.jit', '.bin.index.json', 'model.json', '.ir', 'serialized_exported_program.json', 'serialized_state_dict.json', 'archive_format']
```

Get meta data about format from python:

```python
from thirdparty.pparse.ident.extensions import typedb

print(typedb[args.type_name])
```

## Detect model by extension

Example run:

```sh
$ yannt pparse ident byext /work/models/bert/bert-AutoModel.params.pt
Possible types: ['caffe', 'onnx', 'pickle', 'pytorch', 'sklearn', 'tensorrt', 'tf']
$ yannt pparse ident byext /work/models/bert/test.safetensors
Possible types: ['safetensors']
```

Detect type by extension from python:

```python
from thirdparty.pparse.ident.extensions import typedb, ident_by_extension

filepath = '/work/models/bert/bert-AutoModel.params.pt'
print(f"Possible types: {ident_by_extension(filepath)}")
```
