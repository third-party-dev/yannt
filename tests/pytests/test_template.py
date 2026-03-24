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
import numpy


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

    # #### Snippet For Development Only ####
    # print(f"Locals: {list(locals().keys())}")
    # breakpoint()
    # #### Snippet For Development Only ####

#test_data(None)