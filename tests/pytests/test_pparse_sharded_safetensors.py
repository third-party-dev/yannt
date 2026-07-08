#!/usr/bin/env python3

import pytest
import logging
log = logging.getLogger(__name__)


import os
import json
import numpy
import safetensors
import safetensors.numpy
from thirdparty.pparse.utils import run_test_independently


log.info("\n## Loading imports.")
from thirdparty.pparse.view.safetensors import SafeTensorsIndex


@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def test_data(generated_data_dir):

    tgt_path = "./models/bert/safetensors_sharded/model.safetensors.index.json"

    log.info("\n## Parsing with pparse")
    ppobj = SafeTensorsIndex().open_fpath(tgt_path)

    log.info("\n## Parsing with naive")

    # Upstream safetensors library doesn't do indices. (transformers does though)
    # For this test, we'll use json and safetensors lib iteratively.
    sst_shards = {}
    sst_metadata = {}
    sst_tensors = {}
    with open(tgt_path) as f:
        weight_map = json.load(f)["weight_map"]
    for tensor_name, shard_file in weight_map.items():
        sst_shards.setdefault(shard_file, []).append(tensor_name)
    for shard_file, names in sst_shards.items():
        shard_path = os.path.join(os.path.dirname(tgt_path), shard_file)
        with safetensors.safe_open(shard_path, framework="numpy", device="cpu") as f:
            sst_metadata[shard_file] = f.metadata()
            for name in names:
                sst_tensors[name] = f.get_tensor(name)

    ppkeys = sorted(list(ppobj.tensor_names()))
    sstkeys = sorted(list(sst_tensors.keys()))
    
    log.info(f"\n## Comparing tensor names and weights. (ppkeys {len(ppkeys)} stkeys {len(sstkeys)})")
    assert len(sstkeys) == len(ppkeys)
    for i in range(len(sstkeys)):
        assert ppkeys[i] == sstkeys[i]
        ppnumpy = ppobj.tensor(ppkeys[i]).as_numpy()
        sstnumpy = sst_tensors[sstkeys[i]]
        assert numpy.array_equal(sstnumpy, ppnumpy)


def test_index_cli(generated_data_dir):
    import subprocess
    tgt_path = "./models/bert/safetensors_sharded/model.safetensors.index.json"
    result = subprocess.run(["yannt", "pparse", "safetensors", "index", tgt_path], capture_output=True, text=True)
    # TODO: Verify result.stdout and result.stderr
    assert result.returncode == 0


if __name__ == "__main__":
    run_test_independently(log, [[test_data, [None], None]])