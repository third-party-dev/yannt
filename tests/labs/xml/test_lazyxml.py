#!/usr/bin/env python3

import logging
log = logging.getLogger(__name__)

import thirdparty.pparse.lib as pparse
from thirdparty.pparse.lazy.xml import configure_pparser

class Xml:
    def __init__(self):
        self._extraction = None

    def _parse(self, data_source, fname="unnamed.xml", recursion=None):

        try:
            data_range = pparse.Range(data_source.open(), data_source.length)
            self._extraction = pparse.BytesExtraction(name=fname, reader=data_range)
            parser = configure_pparser()(self._extraction, 'xml')

            self._extraction.add_result('xml', parser.make_root_node())
            self._extraction._result['xml'].load(recursion=recursion)

        except pparse.EndOfDataException as e:
            print(e)
            pass
        except Exception as e:
            print(e)
            import traceback

            traceback.print_exc()

        return self


    def root_node(self):
        return self._extraction._result['xml']


    def open_fpath(self, fpath, recursion=None):
        return self._parse(pparse.FileData(path=fpath), fname=fpath, recursion=recursion)


    def from_bytesio(self, bytes_io, fname="unnamed.xml", recursion=None):
        return self._parse(pparse.BytesIoData(bytes_io=bytes_io), fname=fname, recursion=recursion)


# from thirdparty.pparse.utils import activate_logging
# activate_logging(args)

# from thirdparty.pparse.utils import pparse_repr
# from thirdparty.pparse.view.onnx import Onnx

print(f"Parsing xml.")
import io
xml_obj = Xml().from_bytesio(io.BytesIO('''<?xml version="1.0" encoding="utf-8" ?>
<!-- my test comment -->
<?special other=data ?>
<test myattr="myvalue">text<child><grandchild /></child></test>
<!-- epilog comment -->
'''.encode('utf-8')))

root = xml_obj.root_node()
root.dump()

from thirdparty.pparse.view.xml import ElementTree
et = ElementTree().from_pparse_node(root.value['document'], recursive=True)

breakpoint()
