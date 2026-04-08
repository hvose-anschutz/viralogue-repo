#!/usr/bin/env python3

"""Finds barcodes based on a provided file of reads."""

import subprocess
import sys
import re

#######################################################
#            CLASS / FUNCTION DEFINITIONS             #
#######################################################
def write_out(my_filename: str,
              item_list: list,
              delimiter: str="\n"):
    """writes out a provided list to a specified file."""
    with open(my_filename,"w",encoding="utf-8") as f:
        for item in item_list:
            f.write(item + delimiter)
        f.close()
#######################################################
#                VARIABLE DECLARATION                 #
#######################################################
my_dict = {}
TEST_FASTQ = sys.argv[1]
TEST2_FASTQ = re.sub("_R1","_R2",TEST_FASTQ)
new_r1_file = re.sub(".fastq","_parsed.fastq",TEST_FASTQ)
new_r2_file = re.sub("_R1","_R2",new_r1_file)
TEST_IDS = "test_id.txt"
#######################################################
#                   MAIN FUNCTION                     #
#######################################################

result = subprocess.run(['grep','-A','1','-f',
                        TEST_IDS,
                        TEST_FASTQ,'--no-group-separator'],
                        capture_output=True,
                        text=True,
                        check=False)
fasta = result.stdout.split("\n")

for line in range(0,len(fasta)-1,2):
    my_dict[fasta[line]] = fasta[line+1][0:16]

BARCODE_LIST = "|".join(list(my_dict.values()))
#print(barcode_list)

new_r1_info = subprocess.run(['grep','-B','1','-A','2','-E',
                              BARCODE_LIST,
                              TEST_FASTQ,'--no-group-separator'],
                              capture_output=True,
                              text=True,
                              check=False)
new_r1_lines = new_r1_info.stdout.split("\n")

with open(new_r1_file,"w",encoding="utf-8") as h:
    for items in new_r1_lines:
        h.write(items + "\n")
h.close()

r1_ids = []

for my_id in range(0,len(new_r1_lines),4):
    id_to_add = new_r1_lines[my_id].split(" ")
    r1_ids.append(id_to_add[0])

r1_ids.pop()

IDS_TO_FIND = "|".join(r1_ids)

#print(ids_to_find)

new_r2_info = subprocess.run(['grep','-A','3','-F','-E',IDS_TO_FIND,
                              TEST2_FASTQ,'--no-group-separator'],
                             capture_output=True,
                             text=True,
                             check=False)
new_r2_lines = new_r2_info.stdout.split("\n")
#print(new_r2_lines)

with open(new_r2_file,"w",encoding="utf-8") as g:
    for items2 in new_r2_lines:
        g.write(items2 + "\n")
g.close()
