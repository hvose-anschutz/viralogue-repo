#!/usr/bin/env python3

"""Turns a list of sequences in txt format into a fasta file format."""

import sys

JUST_SEQS = True

with open(sys.argv[1],
          "r",
          encoding="utf-8") as f, open("all_L1HS_RT_full_seqs.fa",
                                       "w",
                                       encoding="utf-8") as o:
    for line in f.readlines():
        my_line = line.strip().split()
        o.write(f">{my_line[0]}\n")
        if JUST_SEQS:
            o.write(f"{my_line[1]}\n")
        else:
            o.write(f"{my_line[3]}\n")
o.close()
f.close()

# with open("all_L1HS_full_seqs.fasta","r",encoding="utf-8") as f:
#     for line in f.readlines():
#         print(line[883:9527])

# f.close()
