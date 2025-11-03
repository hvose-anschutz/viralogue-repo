#!/usr/bin/env python3

"""Searches two paired FASTQ files for a specific Run ID. 
The second file provided will always be faster than the first, 
with the assumption that the byte offset is equal across both files."""

import re
import sys

BC_INTEREST = "id"
FOUND_IT = False
MATCHING_READS = {}
R1_LINES = []
BYTE_OFFSETS = []

with open("test.fastq","r",encoding="utf-8") as f:
    for idx, my_id in enumerate(f.readlines()):
        if (my_id[0] == "@") and (not FOUND_IT):
            if re.search(BC_INTEREST,id) is not None:
                BYTE_OFFSETS.append(idx)
                FOUND_IT = True
                new_key = my_id.strip()
        elif (FOUND_IT) and (len(R1_LINES) < 3):
            R1_LINES.append(my_id.strip())
        elif len(R1_LINES) >= 3:
            FOUND_IT = False
            MATCHING_READS[new_key] = R1_LINES
            R1_LINES = []

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
