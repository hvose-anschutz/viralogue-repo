#!/usr/bin/env python3

"""Creates a list from a tab-delimited file given 
an index to create from. Must be run with Python 3.10+"""

import re

def write_to_file(filename,list_to_write):
    """Writes a provided list into a new file"""
    with open(filename,"w",encoding="utf=8") as g:
        for my_id in list_to_write:
            g.write(my_id + "\n")
    g.close()

MY_READS_L1 = []
MY_READS_L2 = []
MY_READS_L3 = []

with open("mhvy_infected_blastn_3.out","r",encoding="utf-8") as f:
    for match in f.readlines():
        match_info = match.strip().split()
        lane = re.search(r"T3:(\d):",match_info[1])
        match int(lane.group(1)):
            case 1:
                MY_READS_L1.append(match_info[1])
            case 2:
                MY_READS_L2.append(match_info[1])
            case 3:
                MY_READS_L3.append(match_info[1])
f.close()

write_to_file("mhvy_sample3_L001.txt",MY_READS_L1)
write_to_file("mhvy_sample3_L002.txt",MY_READS_L2)
write_to_file("mhvy_sample3_L003.txt",MY_READS_L3)
