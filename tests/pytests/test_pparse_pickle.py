#!/usr/bin/env python3

import pytest
import logging
log = logging.getLogger(__name__)


import io
import pickle
from collections import OrderedDict
from thirdparty.pparse.utils import run_test_independently


log.info("\n## Loading imports.")
from thirdparty.pparse.view.pickle import Pickle

@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def test_data(generated_data_dir):
    buf = io.BytesIO()
    obj = OrderedDict([
        ("key1", "value1"),
        ("key2", ["value2"]),
        ("key3", {"key4": "value4"}),
        ("key5", 5)])
    pickle.dump(obj, buf, protocol=pickle.HIGHEST_PROTOCOL)
    buf.seek(0)

    log.info("\n## Parsing with naive")
    pyod = pickle.load(buf)
    buf.seek(0)

    log.info("\n## Parsing with pparse")
    _ppobj = Pickle().from_bytesio(buf)
    # TODO: A view object should abstract this.
    ppobj = _ppobj._extraction._result["pkl"].value[0].value[0]

    # Note: This is tricky because our pparse output is vastly different
    #       than a normal pickle. Not just because its in a Node tree
    #       like structure, but we've also deferred all module.function
    #       calls. Therefore whether the path goes into a reduce call,
    #       persistent call, a new call, or something else implicit,
    #       the way to reference this can feel relatively radically off.

    # Manually rebuild the OrderedDict:
    arr = [i for i in ppobj.items()]
    arr.reverse()
    ppod = OrderedDict(arr)

    # Now check they are equal (python implicitly does a deep compare)
    assert pyod == ppod


if __name__ == "__main__":
    run_test_independently(log, [[test_data, [None], None]])