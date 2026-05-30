#!/usr/bin/env python3

import sys
from rknn.api import RKNN

rknn = RKNN()
rknn.load_rknn('models/mobilenet_v2_for_rk3562.rknn')
rknn.summary()
breakpoint()
# models/mobilenet_v2_for_rk3562.rknn
# pip uninstall -y setuptools && pip install setuptools==68.2.2


from rknn.api import RKNN

rknn = RKNN()

ret = rknn.load_rknn("model.rknn")
assert ret == 0

# This prints input/output tensor info
print("Inputs:")
for inp in rknn.get_input_shape():
    print(inp)

print("Outputs:")
for out in rknn.get_output_shape():
    print(out)
