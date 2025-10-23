#!/usr/bin/env python3

"""Searches two paired FASTQ files for a specific Run ID. The second file provided will always be faster than the first, with the assumption that
the byte offset is equal across both files."""

import re
import sys

bc_interest = "id"
r1_info = 0
found_it = False
matching_reads = {}
r1_lines = []
byte_offsets = []

with open("test.fastq","r") as f:
    for idx, id in enumerate(f.readlines()):
        if (id[0] == "@") and (found_it == False):
            if re.search(bc_interest,id) is not None:
                #print("found match in " + bc_interest + " and " + id)
                byte_offsets.append(idx)
                found_it = True
                new_key = id.strip()
        elif (found_it == True) and (len(r1_lines) < 3):
            r1_lines.append(id.strip())
        elif len(r1_lines) >= 3:
            found_it = False
            matching_reads[new_key] = r1_lines
            r1_lines = []

f.close()

with open("test2.fastq","r") as g:
    for new_start in byte_offsets:
        #374 is the byte offset for each four line set: 68 + 152 + 2 + 152
        g.seek((new_start/4)*374)
        for idx, info in enumerate(g.readlines()):
            if idx == 0:
                id_key = re.sub("2:N","1:N",info.strip())
                print(id_key)
            elif (idx < 4) and (idx != 0):
                matching_reads[id_key].append(info.strip())
            else:
                break
g.close()

with open("read_info.txt","w") as h:
    for keys, values in matching_reads.items():
        h.write(keys + ":\t" + str(values) + "\n")
h.close()