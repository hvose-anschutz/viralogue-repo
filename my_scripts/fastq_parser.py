#!/usr/bin/env python3

"""Searches two paired FASTQ files for a specific Run ID. 
The second file provided will always be faster than the first, 
with the assumption that the byte offset is equal across both files."""

import re

BC_INTEREST = "id"
found_it = False
MATCHING_READS = {}
r1_lines = []
BYTE_OFFSETS = []

with open("test.fastq","r",encoding="utf-8") as f:
    new_key = []
    for idx, my_id in enumerate(f.readlines()):
        if (my_id[0] == "@") and (not found_it):
            if re.search(BC_INTEREST,id) is not None:
                BYTE_OFFSETS.append(idx)
                found_it = True
                new_key = my_id.strip()
        elif (found_it) and (len(r1_lines) < 3):
            r1_lines.append(my_id.strip())
        elif len(r1_lines) >= 3:
            found_it = False
            MATCHING_READS[new_key] = r1_lines
            r1_lines = []

f.close()

with open("test2.fastq","r",encoding="utf-8") as g:
    for new_start in BYTE_OFFSETS:
        #374 is the byte offset for each four line set:
        #68 + 152 + 2 + 152
        g.seek((new_start/4)*374)
        for idx, info in enumerate(g.readlines()):
            if idx == 0:
                id_key = re.sub("2:N","1:N",info.strip())
                print(id_key)
            elif (idx < 4) and (idx != 0):
                MATCHING_READS[id_key].append(info.strip())
            else:
                break
g.close()

with open("read_info.txt","w",encoding="utf-8") as h:
    for keys,values in MATCHING_READS.items():
        h.write(keys + ":\t" + str(values) + "\n")
h.close()
