trtexec \
  --onnx=model.onnx \
  --saveEngine=model.engine \
  --fp16 \                         # optional: FP16 precision
  --workspace=4096 \               # memory in MB
  --minShapes=input:1x3x224x224 \  # for dynamic shapes
  --optShapes=input:8x3x224x224 \
  --maxShapes=input:16x3x224x224


git lfs install
git lfs track "*.safetensors"
git lfs track "*.tflite"
git lfs track "*.om"
git lfs track "*.mnn"
git lfs track "*.rknn"
git lfs track "*.pt"
git lfs track "*.pb"
git lfs track "*.torchscript"
git lfs track "*.mlmodel"
git lfs track "*.bin"
git lfs track "*.param"
git lfs track "*.pdparams"
git lfs track "*.pdiparams"
git lfs track "*.onnx"


import torch
from ultralytics import YOLO
from safetensors.torch import save_file

# Load model
model = YOLO("yolov5su.pt")

# Extract state dict
state_dict = model.model.state_dict()

# Convert all tensors to float32 (safetensors requires contiguous tensors)
state_dict = {k: v.contiguous().float() for k, v in state_dict.items()}

# Save
save_file(state_dict, "yolov5su.safetensors")
print("Done!")