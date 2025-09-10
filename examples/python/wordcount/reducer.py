#!/usr/bin/env python3
import sys

current = None
total = 0

for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue
    try:
        k, v = line.split("\t", 1)
        v = int(v)
    except Exception:
        continue

    if k != current:
        if current is not None:
            print(f"{current}\t{total}")
        current, total = k, 0
    total += v

if current is not None:
    print(f"{current}\t{total}")
