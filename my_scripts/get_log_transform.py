#!/usr/bin/env python3

"""Calculates the log transform of each line and prints them
to a new file."""

import sys

with open(sys.argv[1],
          "r",
          encoding="utf-8") as f,open("ERV_logs.txt",
                                           "w",
                                           encoding="utf-8") as w:
    for my_line in f.readlines():
        line = my_line.strip().split("\t")
        for i in range(73,len(line)-2,3):
            w.write(line[i] + "\t")
        w.write("\n")
f.close()
w.close()
