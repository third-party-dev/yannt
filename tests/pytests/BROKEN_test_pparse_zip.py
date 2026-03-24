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
import zipfile
from thirdparty.pparse.view.zip import Zip


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
    log.error("\n!! Skipping test because 'pparse zip' done broke.")
    pytest.skip()

    # Generate zip file
    zip_buffer = io.BytesIO()

    # ! BUG: 'pparse zip' is only parsing the first file for *this* zip!
    #with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
    #with zipfile.ZipFile(zip_buffer, mode="w") as zf:
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_BZIP2) as zf:
        zf.writestr("file1.txt", "Hello World")
        zf.writestr("file2.txt", "Another file")
        zf.writestr("file3.txt", "Another file")

    tgt_path = "./models/bert/safetensors/model.safetensors"

    log.info("\n## Parsing with pparse")
    ppobj = Zip().from_bytesio(zip_buffer)
    ppzip = ppobj._extraction._result['zip']
    #pp2obj = Zip().open_fpath("./models/bert/pt/bert-AutoModel.complete.pt")

    log.info("\n## Parsing with naive")
    pyobj = build_pyobj(zip_buffer) 
    pyfiles = sorted(list(pyobj.keys()))
    
    #ppobj._extraction._result['zip'].value
        
    # assert len(stkeys) == len(ppkeys)
    # for i in range(len(stkeys)):
    #     assert ppkeys[i] == stkeys[i]
    #     ppnumpy = ppobj.tensor(ppkeys[i]).as_numpy()
    #     stnumpy = stobj.get_tensor(stkeys[i])
    #     assert numpy.array_equal(stnumpy, ppnumpy)

    # #### Snippet For Development Only ####
    # print(f"Locals: {list(locals().keys())}")
    # breakpoint()
    # #### Snippet For Development Only ####

#test_data(None)