#!/usr/bin/env python3

import re
import my_functions.files.file_funcs as ff


my_SJs = ff.tab_separator("SJtest.txt")
all_SJs = {}

for item in my_SJs:
    new_title = item[0] + ":" + item[1] + "-" + item[2]
    total = int(item[7]) + int(item[8])
    new_accession = "test" + ":" + str(total) + "=u" + item[7] + "+m" + item[8] 

    if new_title not in all_SJs.keys():
        all_SJs[new_title] = [new_accession]
    else:
        all_SJs[new_title].append(new_accession)

ff.write_dict_to_file("allSJ.txt",all_SJs)