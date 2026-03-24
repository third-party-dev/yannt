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
import io
import hashlib
import json
from thirdparty.pparse.view.json import Json


@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def build_pyobj(zip_buffer):
    pyobj = {}
    # Open the ZIP in memory
    with zipfile.ZipFile(zip_buffer, 'r') as zf:
        for file_name in zf.namelist():
            data = zf.read(file_name)
            pyobj[file_name] = hashlib.md5(data).hexdigest()
    return pyobj


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

    # #### Snippet For Development Only ####
    # print(f"Locals: {list(locals().keys())}")
    # breakpoint()
    # #### Snippet For Development Only ####

#test_data(None)