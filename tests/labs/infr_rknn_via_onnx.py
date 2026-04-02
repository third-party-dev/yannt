#!/usr/bin/env python3

import cv2
import numpy as np
from PIL import Image, ImageDraw
from rknn.api import RKNN

ONNX_MODEL = 'yolov5nu.onnx'

rknn = RKNN()

print('Config model')

rknn.config(
    mean_values=[[0,0,0]],
    std_values=[[255,255,255]],
    target_platform='rk3588'   # still required
)

print('Load ONNX')

ret = rknn.load_onnx(model=ONNX_MODEL)
assert ret == 0

print('Build model')

ret = rknn.build(do_quantization=False)
assert ret == 0

print('Init runtime (SIMULATOR)')

ret = rknn.init_runtime()
assert ret == 0

print('Load image')
IMAGE_PATH='bus.jpg'
img = cv2.imread(IMAGE_PATH)
img = cv2.resize(img, (640,640))
img = np.expand_dims(img, 0)

print('Run inference')

outputs = rknn.inference(inputs=[img])

print('Output tensors:', len(outputs))

for i, out in enumerate(outputs):
    print(f'Output {i}: {out.shape}')

rknn.release()

print('Done')

# --------------------------------------------------
# Outputs interpretation and box drawing done w/ LLM
# --------------------------------------------------

# Parameters
CONF_THRES = 0.25
IOU_THRES = 0.45
IMG_SIZE = 640

# Get predictions
pred = outputs[0][0].T  # (8400, 84)

boxes = []
scores = []
class_ids = []

for row in pred:
    x, y, w, h = row[:4]
    class_scores = row[4:]

    class_id = np.argmax(class_scores)
    score = class_scores[class_id]

    if score < CONF_THRES:
        continue

    # Convert xywh → xyxy
    x1 = x - w / 2
    y1 = y - h / 2
    x2 = x + w / 2
    y2 = y + h / 2

    boxes.append([x1, y1, x2, y2])
    scores.append(score)
    class_ids.append(class_id)

boxes = np.array(boxes)
scores = np.array(scores)

# NMS
def compute_iou(box, boxes):
    x1 = np.maximum(box[0], boxes[:,0])
    y1 = np.maximum(box[1], boxes[:,1])
    x2 = np.minimum(box[2], boxes[:,2])
    y2 = np.minimum(box[3], boxes[:,3])

    inter = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)

    area1 = (box[2]-box[0])*(box[3]-box[1])
    area2 = (boxes[:,2]-boxes[:,0])*(boxes[:,3]-boxes[:,1])

    union = area1 + area2 - inter

    return inter / union

keep = []

idxs = scores.argsort()[::-1]

while len(idxs) > 0:
    i = idxs[0]
    keep.append(i)

    if len(idxs) == 1:
        break

    ious = compute_iou(boxes[i], boxes[idxs[1:]])

    idxs = idxs[1:][ious < IOU_THRES]

boxes = boxes[keep]
scores = scores[keep]
class_ids = [class_ids[i] for i in keep]

print("Detections:", len(boxes))

# Draw boxes on original image
orig = Image.open(IMAGE_PATH).convert("RGB")
draw = ImageDraw.Draw(orig)

scale_x = orig.width / IMG_SIZE
scale_y = orig.height / IMG_SIZE

for box, score, cid in zip(boxes, scores, class_ids):

    x1, y1, x2, y2 = box

    x1 *= scale_x
    x2 *= scale_x
    y1 *= scale_y
    y2 *= scale_y

    draw.rectangle(
        [x1, y1, x2, y2],
        outline="red",
        width=2
    )

# Save result
orig.save("result.jpg")

print("Saved result.jpg")
