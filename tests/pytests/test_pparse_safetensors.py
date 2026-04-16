#!/usr/bin/env python3

import pytest
import logging
log = logging.getLogger(__name__)


import numpy
import safetensors
import safetensors.numpy
from thirdparty.pparse.utils import run_test_independently


log.info("\n## Loading imports.")
from thirdparty.pparse.view.safetensors import SafeTensors


@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def test_data(generated_data_dir):

    tgt_path = "./models/bert/safetensors/model.safetensors"

    log.info("\n## Parsing with pparse")
    ppobj = SafeTensors().open_fpath(tgt_path)
    log.info("\n## Parsing with naive")
    stobj = safetensors.safe_open(tgt_path, framework="numpy", device="cpu")

    stkeys = sorted(list(stobj.keys()))
    ppkeys = ppobj.tensor_names()
    
    log.info(f"\n## Comparing tensor names and weights. (ppkeys {len(ppkeys)} stkeys {len(stkeys)})")
    assert len(stkeys) == len(ppkeys)
    for i in range(len(stkeys)):
        assert ppkeys[i] == stkeys[i]
        ppnumpy = ppobj.tensor(ppkeys[i]).as_numpy()
        stnumpy = stobj.get_tensor(stkeys[i])
        assert numpy.array_equal(stnumpy, ppnumpy)


if __name__ == "__main__":
    run_test_independently(log, [[test_data, [None], None]])