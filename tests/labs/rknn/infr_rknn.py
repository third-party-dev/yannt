#!/usr/bin/env python3

import cv2
import numpy as np
from rknn.api import RKNN

RKNN_MODEL = 'yolov5nu.rknn'
IMAGE_PATH = 'bus.jpg'

rknn = RKNN()

print('Load RKNN')
ret = rknn.load_rknn(RKNN_MODEL)
assert ret == 0

print('Init runtime (SIMULATOR)')
ret = rknn.init_runtime()
assert ret == 0

# Load image
img = cv2.imread(IMAGE_PATH)

img = cv2.resize(img, (640, 640))
img = np.expand_dims(img, 0)

print('Running inference...')
outputs = rknn.inference(inputs=[img])

print('Output tensor count:', len(outputs))

for i, out in enumerate(outputs):
    print(f'Output {i}: shape={out.shape}')

rknn.release()
