#!/usr/bin/env python3

import pytest
import logging
log = logging.getLogger(__name__)


import io
import hashlib
import json
from thirdparty.pparse.utils import run_test_independently


log.info("\n## Loading imports under test.")
from thirdparty.pparse.view.json import Json


@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def test_data(generated_data_dir):
    json_string = b'''
        {"key1": "value1", "key2": ["value2"], "key3": {"key4": "value4"}, "key5": 5 }
    '''
    json_buffer = io.BytesIO()
    json_buffer.write(json_string)

    log.info("\n## Parsing with pparse")
    ppobj = Json().from_bytesio(json_buffer, fname="test.json")
    ppjson = ppobj._extraction._result['json'].value.value

    log.info("\n## Parsing with naive")
    pyobj = json.loads(json_string)

    # TODO: We should convert Node tree to a JSON string, but for now we'll
    # TODO: hard code everything so we can have a repeatable test.

    log.info("\n## Checking pparse and naive see same data")
    assert ppjson['key1'] == pyobj['key1']
    assert ppjson['key2'].value[0] == pyobj['key2'][0]
    assert ppjson['key3'].value['key4'] == pyobj['key3']['key4']
    assert ppjson['key5'] == pyobj['key5']


if __name__ == "__main__":
    run_test_independently(log, [[test_data, [None], None]])