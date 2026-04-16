#!/usr/bin/env python3

import pytest
import logging
log = logging.getLogger(__name__)


import io
import hashlib
import zipfile
import safetensors
import safetensors.numpy
from thirdparty.pparse.utils import run_test_independently


log.info("\n## Loading imports.")
from thirdparty.pparse.view.safetensors import SafeTensors
from thirdparty.pparse.view.zip import Zip


@pytest.fixture(scope="session")
def generated_data_dir():
    # TODO: Verify we have hft.
    # TODO: On error: pytest.fail(f"Test data generation failed: {e}")
    # TODO: Generate the test data here.
    return None


def test_data(generated_data_dir):
    # log.error("\n!! Skipping test because 'pparse zip' done broke.")
    # pytest.skip()

    # Generate zip file
    zip_buffer = io.BytesIO()

    # TODO: Add support for BZIP, LZMA, and other compression formats. (ZSTD?)
    # TODO: Add checks for FOOTER META and FOOTER CRC32.
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("file1.txt", "Hello World")
        zf.writestr("file2.txt", "Another file")
        zf.writestr("file3.txt", "Another file")

    log.info("\n## Parsing with pparse")
    ppobj = Zip().from_bytesio(zip_buffer)
    # TODO: Abstract this in view class
    ppzip = ppobj._extraction._result['zip']
    ppmap = {}
    for fentry in ppzip.value:
        data = fentry.value['decomp_data'].value.getvalue()
        ppmap[fentry.value['fname']] = hashlib.md5(data).hexdigest()
    ppfiles = sorted(list(ppmap.keys()))

    log.info("\n## Parsing with naive")
    pymap = {}
    # Open the ZIP in memory
    with zipfile.ZipFile(zip_buffer, 'r') as zf:
        for file_name in zf.namelist():
            data = zf.read(file_name)
            pymap[file_name] = hashlib.md5(data).hexdigest()
    pyfiles = sorted(list(pymap.keys()))
    
    # Check file entry length matches.
    assert len(ppfiles) == len(pyfiles)
    for i in range(len(pyfiles)):
        # Check the file content (via MD5)
        assert pymap[pyfiles[i]] == ppmap[ppfiles[i]]


if __name__ == "__main__":
    run_test_independently(log, [[test_data, [None], None]])