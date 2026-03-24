#!/usr/bin/env python3

import pytest
import logging

log = logging.getLogger(__name__)

# #### Snippet For Development Only ####
# import sys
# handler = logging.StreamHandler(sys.stdout)
# fmt = "%(asctime)s [%(levelname)s] %(message)s"
# logging.basicConfig(level=logging.INFO, format=fmt, handlers=[handler])
# #### Snippet For Development Only ####

log.info("\n## Loading imports.")
from thirdparty.pparse.view.pytorch import PyTorch
import torch
import numpy


@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def test_data(generated_data_dir):

    tgt_path = "./models/bert/pt/bert-AutoModel.complete.pt"
    log.info("\n## Parsing with pparse")
    ppobj = PyTorch().open_fpath(tgt_path)
    log.info("\n## Parsing with torch")
    ptobj = torch.load(tgt_path, map_location="cpu", weights_only=False)

    ppkeys = sorted(ppobj.tensor_names())        
    ptparams = dict(ptobj.named_parameters())
    ptkeys = sorted(list(ptparams.keys()))

    log.info(f"\n## Comparing tensor names and weights (ppkeys {len(ppkeys)} ptkeys {len(ptkeys)}).")
    assert len(ppkeys) == len(ptkeys)
    for i in range(len(ptkeys)):
        # TODO: Check shape first?
        assert ppkeys[i] == ptkeys[i]
        ptnumpy = ptparams[ptkeys[i]].detach().numpy()
        ppnumpy = ppobj.tensor(ppkeys[i]).as_numpy()
        assert numpy.array_equal(ptnumpy, ppnumpy)

    # #### Snippet For Development Only ####
    # print(f"Locals: {list(locals().keys())}")
    # breakpoint()
    # #### Snippet For Development Only ####

# test_data(None)