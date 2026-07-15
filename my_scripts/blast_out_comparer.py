#!/usr/bin/env python3

"""Interprets outfmt files from BLAST to compare regions"""

import sys

with open(sys.argv[1],"r",encoding="utf-8") as f:
    for line in f.readlines():
        my_line = line.strip().split()
