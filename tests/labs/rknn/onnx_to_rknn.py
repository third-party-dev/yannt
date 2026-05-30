#!/usr/bin/env python3

from rknn.api import RKNN

ONNX_MODEL = 'yolov5nu.onnx'
RKNN_MODEL = 'yolov5nu.rknn'

rknn = RKNN()

print('Config model')
rknn.config(
    mean_values=[[0, 0, 0]],
    std_values=[[255, 255, 255]],
    target_platform='rk3588'
)

print('Loading ONNX')
ret = rknn.load_onnx(
    model=ONNX_MODEL,
    inputs=['images'],
    input_size_list=[[1, 3, 640, 640]]
)
assert ret == 0

print('Building RKNN')
ret = rknn.build(do_quantization=False)
assert ret == 0

print('Export RKNN')
ret = rknn.export_rknn(RKNN_MODEL)
assert ret == 0

rknn.release()

print('Done')
