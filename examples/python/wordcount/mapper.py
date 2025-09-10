#!/usr/bin/env python3
import sys

for line in sys.stdin:
    for w in line.strip().split():
        if w:
            print(f"{w}\t1")
