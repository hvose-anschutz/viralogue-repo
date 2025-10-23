#!/usr/bin/env python3

"""Creates a list from a tab-delimited file given an index to create from."""

import re

def write_to_file(filename,list_to_write):
    with open(filename,"w") as g:
        for id in list_to_write:
            g.write(id + "\n")
    g.close()

my_reads_L1 = []
my_reads_L2 = []
my_reads_L3 = []

with open("mhvy_infected_blastn_3.out","r") as f:
    for match in f.readlines():
        match_info = match.strip().split()
        lane = re.search("T3:(\d):",match_info[1])
        match int(lane.group(1)):
            case 1:
                my_reads_L1.append(match_info[1])
            case 2:
                my_reads_L2.append(match_info[1])
            case 3:
                my_reads_L3.append(match_info[1])
f.close()

write_to_file("mhvy_sample3_L001.txt",my_reads_L1)
write_to_file("mhvy_sample3_L002.txt",my_reads_L2)
write_to_file("mhvy_sample3_L003.txt",my_reads_L3)
