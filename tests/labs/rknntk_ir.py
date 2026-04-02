#!/usr/bin/env python3

# Note: rknn-toolkit2 uses onnx==1.16.1, NOT onnx==1.19.1
# Note: rknn-toolkit2 requires torch 2.4.0 for py3.9
# Note: rknn-toolkit (v1) uses pytorch 1.x
# Note: onnx with opset 14 has proven to work for yolov5nu
# Note: rknn-toolkit2 simulator requires IR (rknn file no good)

from pprint import pprint
import numpy as np
from rknn.api import RKNN

# Initialize the toolkit object
rknn = RKNN()
# Configure the toolkit object
rknn.config(
  mean_values=[[0,0,0]],
  std_values=[[255,255,255]],
  # also required for simulator
  target_platform='rk3588'
)
# Load the model
rknn.load_onnx(model='yolov5nu.onnx')
# Build the IR and model object
rknn.build(do_quantization=False)


# Here is where we have full access to the IR
pprint(rknn.rknn_base.ir.node)
breakpoint()


# To inference, you'd then do.
#rknn.init_runtime()
#outputs = rknn.inference(inputs=[img])

