#!/usr/bin/env python3
"""
Reducer aggregates contributions and reconstructs adjacency list.
Env:
- N: number of nodes (required to add base rank (1-d)/N)
- DAMPING: optional damping factor (default 0.85)
"""
import os
import sys

try:
    N = int(os.environ.get("N", "0"))
except ValueError:
    N = 0

try:
    DAMPING = float(os.environ.get("DAMPING", "0.85"))
except ValueError:
    DAMPING = 0.85

BASE = (1.0 - DAMPING) / N if N > 0 else 0.0

def emit(node, total_contrib, adjacency):
    pr = BASE + DAMPING * total_contrib
    adj_str = ",".join(adjacency) if isinstance(adjacency, list) else (adjacency or "")
    print(f"{node}\t{pr}\t{adj_str}")

current = None
adj = None
sum_contrib = 0.0

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) < 3:
        continue
    node, tag, value = parts[0], parts[1], parts[2]

    if current is None:
        current = node
    if node != current:
        emit(current, sum_contrib, adj)
        current = node
        adj = None
        sum_contrib = 0.0

    if tag == "ADJ":
        adj = value
    elif tag == "CONTRIB":
        try:
            sum_contrib += float(value)
        except Exception:
            pass

# flush last
if current is not None:
    emit(current, sum_contrib, adj)
