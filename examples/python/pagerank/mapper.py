#!/usr/bin/env python3
"""
Input line format: node\tPR\tcomma_separated_neighbors
Emits contributions to neighbors and also passes adjacency list forward.
"""
import sys

DAMPING = 0.85

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) < 2:
        continue
    node = parts[0]
    try:
        pr = float(parts[1])
    except Exception:
        continue
    neigh = parts[2] if len(parts) > 2 else ""
    neighbors = [n for n in neigh.split(",") if n]

    # Pass adjacency list forward
    print(f"{node}\tADJ\t{neigh}")

    # Dangling node: no outgoing links => no contributions
    if not neighbors:
        continue

    contrib = pr / len(neighbors)
    for v in neighbors:
        print(f"{v}\tCONTRIB\t{contrib}")
