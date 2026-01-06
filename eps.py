#!/usr/bin/env python3

import importlib.metadata as md

for ep in md.entry_points(group="yannt.commands"):
    print(ep.name, "->", ep.value)
