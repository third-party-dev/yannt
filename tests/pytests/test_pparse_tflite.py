#!/usr/bin/env python3

import pytest
import logging
import numpy
log = logging.getLogger(__name__)
from thirdparty.pparse.utils import run_test_independently


log.info("\n## Loading imports under test.")
import tflite
import flatbuffers
from thirdparty.pparse.view.tflite import TFLite


@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def test_data(generated_data_dir):

    tgt_path = "./models/yolov5su_float32.tflite"

    log.info("\n## Parsing with pparse")
    ppobj = TFLite().open_fpath(tgt_path)
    log.info("\n## Parsing with naive")
    with open(tgt_path, "rb") as f:
        tfobj = tflite.Model.GetRootAsModel(f.read(), 0)
    tfgraph = tfobj.Subgraphs(0)

    # Check the tensor count.
    assert tfgraph.TensorsLength() == len(ppobj.tensor_names())

    tfmap = {}
    for idx in range(tfobj.Subgraphs(0).TensorsLength()):
        tensor = tfobj.Subgraphs(0).Tensors(idx)
        tfmap[tensor.Name().decode('utf-8')] = tensor
        # tfobj.Subgraphs(0).Tensors(1).Buffer()

    # Check the tensor names.
    tfkeys = sorted(list(tfmap.keys()))
    ppkeys = sorted(ppobj.tensor_names())

    for idx in range(len(tfkeys)):
        tftensor = tfmap[tfkeys[idx]]
        pptensor = ppobj.tensor(ppkeys[idx])

        # Check the tensor data.
        tfdata = tfobj.Buffers(tftensor.Buffer()).DataAsNumpy()
        ppbytes = pptensor.get_data_bytes()
        # Note: If there is no data, tflite returns DataAsNumpy with 0.
        if len(ppbytes) == 0:
            ppdata = 0
        else:
            ppdata = numpy.frombuffer(pptensor.get_data_bytes(), dtype=numpy.uint8)

        assert numpy.array_equal(tfdata, ppdata)


def test_view_cli(generated_data_dir):
    import subprocess
    tgt_path = "./models/yolov5su_float32.tflite"
    result = subprocess.run(["yannt", "pparse", "tflite", "view", tgt_path], capture_output=True, text=True)
    # TODO: Verify result.stdout and result.stderr
    assert result.returncode == 0


if __name__ == "__main__":
    run_test_independently(log, [[test_data, [None], None]])


