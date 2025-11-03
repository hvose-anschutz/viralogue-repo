#!/usr/bin/env python3
"""Analyzes splice junctions and writes out files in a single-line
interpretations of matches and gaps."""

import my_functions.files.file_funcs as ff
my_sj = ff.tab_separator("SJtest.txt")
ALL_SJ = {}

for item in my_sj:
    new_title = item[0] + ":" + item[1] + "-" + item[2]
    total = int(item[7]) + int(item[8])
    new_accession = "test" + ":" + str(total) + "=u" + item[7] + "+m" + item[8]

    if new_title not in ALL_SJ:
        ALL_SJ[new_title] = [new_accession]
    else:
        ALL_SJ[new_title].append(new_accession)

ff.write_dict_to_file("allSJ.txt",ALL_SJ)
