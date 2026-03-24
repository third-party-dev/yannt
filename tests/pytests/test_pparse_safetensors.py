#!/usr/bin/env python3

import pytest
import logging

log = logging.getLogger(__name__)
from thirdparty.pparse.view import SafeTensors
import safetensors
import safetensors.numpy

# #### Snippet For Development Only ####
# import sys
# handler = logging.StreamHandler(sys.stdout)
# fmt = "%(asctime)s [%(levelname)s] %(message)s"
# logging.basicConfig(level=logging.INFO, format=fmt, handlers=[handler])
# #### Snippet For Development Only ####

log.info("\n## Loading imports.")
import numpy


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

    # #### Snippet For Development Only ####
    # print(f"Locals: {list(locals().keys())}")
    # breakpoint()
    # #### Snippet For Development Only ####

#test_data(None)