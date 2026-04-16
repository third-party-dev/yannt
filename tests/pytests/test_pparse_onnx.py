#!/usr/bin/env python3

import pytest
import logging
log = logging.getLogger(__name__)
from thirdparty.pparse.utils import run_test_independently


log.info("\n## Loading imports under test.")
import numpy
import onnx
from thirdparty.pparse.view.onnx import Onnx


@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def test_data(generated_data_dir):

    tgt_path = "./models/yolo/yolov5su.onnx"

    log.info("\n## Parsing with pparse")
    ppobj = Onnx().open_fpath(tgt_path)
    log.info("\n## Parsing with naive")
    msobj = onnx.load(tgt_path)

    msmap = {}
    for entry in msobj.graph.initializer:
        msmap[entry.name] = entry
    mskeys = sorted([en.name for en in msobj.graph.initializer])
    ppkeys = sorted(ppobj.tensor_names())
    
    log.info(f"\n## Comparing tensor names and weights. (ppkeys {len(ppkeys)} stkeys {len(mskeys)})")
    assert len(mskeys) == len(ppkeys)
    for i in range(len(mskeys)):
        assert ppkeys[i] == mskeys[i]
        #log.info(f"Comparing tensor: {mskeys[i]}.")
        ppnumpy = ppobj.tensor(ppkeys[i]).as_numpy()
        msnumpy = onnx.numpy_helper.to_array(msmap[mskeys[i]])
        assert numpy.array_equal(msnumpy, ppnumpy)


if __name__ == "__main__":
    run_test_independently(log, [[test_data, [None], None]])


