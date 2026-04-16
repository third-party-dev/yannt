#!/usr/bin/env python3

import pytest
import logging
log = logging.getLogger(__name__)


import numpy
from thirdparty.pparse.utils import run_test_independently


log.info("\n## Loading imports.")
from thirdparty.pparse.view.pytorch import PyTorch
import torch


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


if __name__ == "__main__":
    run_test_independently(log, [[test_data, [None], None]])