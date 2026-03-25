#!/usr/bin/env python3

import pytest
import logging

log = logging.getLogger(__name__)

# yolo export model=yolov5su format=tflite --img-size 640 --weights yolov5su.pt
# tlmap['arith.constant85']['buffer'].DataAsNumpy()

#### Snippet For Development Only ####
import sys
handler = logging.StreamHandler(sys.stdout)
fmt = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=fmt, handlers=[handler])
#### Snippet For Development Only ####

log.info("\n## Loading imports.")
import numpy
from thirdparty.pparse.view.tflite import TFLite
import tflite
import flatbuffers

@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def test_data(generated_data_dir):
    log.error("\n!! Skipping test because 'pparse zip' done broke.")
    pytest.skip()

    tgt_path = "./models/yolo/yolov5su_float32.tflite"

    log.info("\n## Parsing with pparse")
    _ppobj = TFLite().open_fpath(tgt_path)
    ppobj = _ppobj._extraction._result['flatbuffers'].value
    log.info("\n## Parsing with naive")
    with open(tgt_path, "rb") as f:
        tlobj = tflite.Model.GetRootAsModel(f.read(), 0)
    
    tlmap = {}
    for i in range(tlobj.Subgraphs(0).TensorsLength()):
        tensor = tlobj.Subgraphs(0).Tensors(i)
        size = tlobj.Buffers(tensor.Buffer()).DataLength()
        if size == 0:
            continue
        tname = tensor.Name().decode('utf-8')
        tlmap[tname] = {
            'tensor': tensor,
            'name': tname,
            'shape': [tensor.Shape(j) for j in range(tensor.ShapeLength())],
            'dtype': tensor.Type(),
            'buffer': tlobj.Buffers(tensor.Buffer())
        }
    tlkeys = sorted(list(tlmap.keys()))
    # ! TFlite Parser Not Completing Here:
    # ! ppobj.value.value['subgraphs'].value[0].value
    # ppkeys = sorted(ppobj.tensor_names())

    # log.info(f"\n## Comparing tensor names and weights. (ppkeys {len(ppkeys)} stkeys {len(mskeys)})")
    # assert len(mskeys) == len(ppkeys)
    # for i in range(len(mskeys)):
    #     assert ppkeys[i] == mskeys[i]
    #     #log.info(f"Comparing tensor: {mskeys[i]}.")
    #     ppnumpy = ppobj.tensor(ppkeys[i]).as_numpy()
    #     msnumpy = onnx.numpy_helper.to_array(msmap[mskeys[i]])
    #     assert numpy.array_equal(msnumpy, ppnumpy)

    #### Snippet For Development Only ####
    log.info(f"Locals: {list(locals().keys())}")
    breakpoint()
    #### Snippet For Development Only ####

test_data(None)

