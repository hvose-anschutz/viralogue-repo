#!/usr/bin/env python3

"""Formats fasta files to be dual-line documents."""

import sys

my_title = ""
curr_seq = ""
final_list = {}

with open(sys.argv[1],"r",encoding="utf-8") as g:
    for idx, fasta_line in enumerate(g.readlines()):
        if fasta_line[0] == ">":
            if idx != 0:
                #need to put everything in line
                final_list[my_title] = curr_seq
                my_title = fasta_line
                curr_seq = ""
            else:
                my_title = fasta_line
        else:
            curr_seq = curr_seq + fasta_line.strip()
g.close()
final_list[my_title] = curr_seq

with open("Hsap38_formatted.fa","w",encoding="utf-8") as h:
    for key, value in final_list.items():
        h.write(f"{key}{value}\n")
h.close()
