#!/usr/bin/env python3
"""
Reads adjacency list lines: node<TAB>n1,n2,...
Emits: node<TAB>PR<TAB>n1,n2,... with PR initialized from env PR0 (default 1.0)
"""
import os, sys

PR0 = float(os.environ.get("PR0", "1.0"))

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if "\t" in line:
        node, neigh = line.split("\t", 1)
    else:
        node, neigh = line, ""
    print(f"{node}\t{PR0}\t{neigh}")
