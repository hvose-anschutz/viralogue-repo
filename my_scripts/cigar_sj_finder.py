#!/usr/bin/env python3

import re
import my_functions.files.file_funcs as mf

#processing: awk '$4 && $6 ~ /N/' should give the fourth (POS) and sixth (CIGAR) columns, tab delimited (ideally)

with open("my_cigar.txt","r") as f:
    my_cigars = f.readlines()
f.close()

print(my_cigars)
my_sjs = {}

for proc_line in my_cigars:
    line = proc_line.strip().split(" ")
    sj_start = None
    sj_end = None
    start_pos = int(line[0])

    unwrap = re.findall("((\d+)(\w))",line[1])

    for item in unwrap:
        if re.search("[DIM]",item[0]) is not None:
            start_pos = start_pos + int(item[1])
        elif re.search("N",item[0]) is not None:
            sj_start = start_pos
            sj_end = sj_start + int(item[1])
            break
    
    my_sj = str(sj_start) + "-" + str(sj_end)

    if my_sj not in my_sjs.keys():
        my_sjs[my_sj] = 1
    else:
        my_sjs[my_sj] += 1

with open("my_final_sjs.txt","w") as g:
    for keys,values in my_sjs.items():
        g.write(keys + " " + str(values) + "\n")
