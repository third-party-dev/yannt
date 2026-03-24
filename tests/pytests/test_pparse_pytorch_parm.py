#!/usr/bin/env python3

import pytest
import logging

log = logging.getLogger(__name__)

log.info("\n## Loading imports.")
from thirdparty.pparse.view.pytorch import PyTorch
import torch
import numpy


@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    # deferred
    return None


def test_data(generated_data_dir):

    tgt_path = "./models/bert/pt/bert-AutoModel.params.pt"
    log.info("\n## Parsing with pparse")
    ppobj = PyTorch().open_fpath(tgt_path)
    log.info("\n## Parsing with torch")
    ptobj = torch.load(tgt_path, map_location="cpu", weights_only=True)

    ppkeys = sorted(ppobj.tensor_names())
    ptkeys = sorted(list(ptobj.keys()))

    log.info(f"\n## Comparing tensor names and weights. (ppkeys {len(ppkeys)} ptkeys {len(ptkeys)})")
    assert len(ppkeys)==len(ptkeys)
    for i in range(len(ptkeys)):
        # TODO: Check shape first?
        assert ppkeys[i] == ptkeys[i]
        ptnumpy = ptobj[ptkeys[i]].numpy()
        ppnumpy = ppobj.tensor(ppkeys[i]).as_numpy()
        assert numpy.array_equal(ptnumpy, ppnumpy)

    # #### Snippet For Development Only ####
    # print(f"Locals: {list(locals().keys())}")
    # breakpoint()
    # #### Snippet For Development Only ####


