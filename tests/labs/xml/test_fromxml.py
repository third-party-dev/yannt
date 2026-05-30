#!/usr/bin/env python3

from thirdparty.pparse._xml import XmlNode
import thirdparty.pparse.lib as pparse


with open("docs/notes/import.xml", "r") as fobj:
    pparse_xml = pparse.PparseXml.from_xml(fobj.read())

print(f"We should have extraction! {globals().keys()}")
breakpoint()

