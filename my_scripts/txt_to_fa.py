#!/usr/bin/env python3

"""Turns a list of sequences in txt format into a fasta file format."""

# with open("all_pol_fastas.txt","r",encoding="utf-8") as f,
# open("all_pol_fastas.fa","w",encoding="utf-8") as o:
#     for line in f.readlines():
#         my_line = line.strip().split()
#         o.write(f">{my_line[0]}_{my_line[1]}\n")
#         o.write(f"{my_line[3]}\n")
# o.close()
# f.close()

with open("maybe_HERVH.fasta","r",encoding="utf-8") as f:
    for line in f.readlines():
        print(line[883:9527])

f.close()
