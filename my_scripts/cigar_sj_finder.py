#!/usr/bin/env python3

"""Processes CIGAR strings from a given list."""

import re

with open("my_cigar.txt","r",encoding="utf-8") as f:
    my_cigars = f.readlines()
f.close()

print(my_cigars)
my_sjs = {}

for proc_line in my_cigars:
    line = proc_line.strip().split(" ")
    sj_start = None
    sj_end = None
    start_pos = int(line[0])

    unwrap = re.findall(r"((\d+)(\w))",line[1])

    for item in unwrap:
        if re.search(r"[DIM]",item[0]) is not None:
            start_pos = start_pos + int(item[1])
        elif re.search("N",item[0]) is not None:
            sj_start = start_pos
            sj_end = sj_start + int(item[1])
            break

    my_sj = str(sj_start) + "-" + str(sj_end)

    if my_sj not in my_sjs:
        my_sjs[my_sj] = 1
    else:
        my_sjs[my_sj] += 1

with open("my_final_sjs.txt","w",encoding="utf-8") as g:
    for keys,values in my_sjs.items():
        g.write(keys + " " + str(values) + "\n")
