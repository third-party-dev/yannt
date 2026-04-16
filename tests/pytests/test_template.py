#!/usr/bin/env python3

import pytest
import logging
log = logging.getLogger(__name__)


import numpy
from thirdparty.pparse.utils import run_test_independently


log.info("\n## Loading imports.")


@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def test_data(generated_data_dir):

    tgt_path = "./models/path/to/model"
    log.info("\n## Parsing with pparse")
    # TODO: Parse with pparse here.
    log.info("\n## Parsing with naive")
    # TODO: Parsing with naive process.
    
    # TODO: Do assertions here.
    assert True


if __name__ == "__main__":
    run_test_independently(log, [[test_data, [None], None]])