#!/usr/bin/env python3

import enum
import subprocess
import sys
import re

#######################################################
#            CLASS / FUNCTION DEFINITIONS             #
#######################################################
def write_out(filename: str,item_list: list, delimiter: str="\n"):
    with open(filename,"w") as f:
        for item in item_list:
            f.write(item_list + delimiter)
    f.close()
#######################################################
#                VARIABLE DECLARATION                 #
#######################################################
my_dict = {}
test_fastq = sys.argv[1]
test2_fastq = re.sub("_R1","_R2",test_fastq)
new_r1_file = re.sub(".fastq","_parsed.fastq",test_fastq)
new_r2_file = re.sub("_R1","_R2",new_r1_file)
test_ids = "test_id.txt"
#######################################################
#                   MAIN FUNCTION                     # 
#######################################################

result = subprocess.run(['grep','-A','1', '-f',test_ids,test_fastq,'--no-group-separator'],capture_output=True,text=True)
fasta = result.stdout.split("\n")

for line in range(0,len(fasta)-1,2):
    my_dict[fasta[line]] = fasta[line+1][0:16] #generates barcodes based on IDs

barcode_list = "|".join(list(my_dict.values()))
#print(barcode_list)

new_r1_info = subprocess.run(['grep','-B','1','-A','2','-E',barcode_list,test_fastq,'--no-group-separator'],capture_output=True,text=True)
new_r1_lines = new_r1_info.stdout.split("\n")

with open(new_r1_file,"w") as f:
    for items in new_r1_lines:
        f.write(items + "\n")
f.close()

r1_ids = []

for id in range(0,len(new_r1_lines),4):
    id_to_add = new_r1_lines[id].split(" ")
    r1_ids.append(id_to_add[0])

r1_ids.pop()

ids_to_find = "|".join(r1_ids)

#print(ids_to_find)

new_r2_info = subprocess.run(['grep','-A','3','-F','-E',ids_to_find,test2_fastq,'--no-group-separator'],capture_output=True,text=True)
new_r2_lines = new_r2_info.stdout.split("\n")
#print(new_r2_lines)

with open(new_r2_file,"w") as g:
    for items2 in new_r2_lines:
        g.write(items2 + "\n")
g.close()
