#!/usr/bin/env python3

"""Generates a consensus sequence for a provided motif list, centered around the "DD" motif
in the active sequence."""

import re
import sys

print("are we even running")

ANCHOR = True
#motif_file = "palm_domains/shorter_motifs/MMERV_shorter_motifs.txt"
motif_file = sys.argv[1]

if ANCHOR:
    valid_dd_patterns = ["GATGAT", "GATGAC", "GACGAT", "GACGAC"]

    VALID_SEQ="|".join(valid_dd_patterns)

    FRONT_HALVES = []
    BACK_HALVES = []
    MOTIF = "MMTV"

    multi_dd = re.compile(VALID_SEQ)

    with open(motif_file,"r",encoding="utf-8") as f:
        for line in f.readlines():
            my_line = line.strip().split()
            #print(my_line)
            dd_match = multi_dd.search(my_line[1])
            #print(dd_match.start())
            BACK_HALVES.append(my_line[1][dd_match.start():])
            front_half = my_line[1][:dd_match.start()]
            FRONT_HALVES.append(front_half[::-1])
    f.close()

    BASE_MAP = {0:"A",1:"C",2:"G",3:"T",4:"-"}

    front_counts = [[0,0,0,0] for _ in range(len(max(FRONT_HALVES,key=len)))]
    back_counts = [[0,0,0,0] for _ in range(len(max(BACK_HALVES,key=len)))]
    f_con_seq = ""
    b_con_seq = ""

    for fseq in FRONT_HALVES:
        for idx,fbase in enumerate(fseq):
            match fbase:
                case "A":
                    front_counts[idx][0] += 1
                case "C":
                    front_counts[idx][1] += 1
                case "G":
                    front_counts[idx][2] += 1
                case "T":
                    front_counts[idx][3] += 1
                case "-":
                    #front_counts[idx][4] += 1
                    pass
                case _:
                    print(f"encountered invalid base {fbase}. Exiting.")
                    sys.exit(1)

    for bseq in BACK_HALVES:
        for idx,bbase in enumerate(bseq):
            match bbase:
                case "A":
                    back_counts[idx][0] += 1
                case "C":
                    back_counts[idx][1] += 1
                case "G":
                    back_counts[idx][2] += 1
                case "T":
                    back_counts[idx][3] += 1
                case "-":
                    #back_counts[idx][4] += 1
                    pass
                case _:
                    print(f"encountered invalid base {bbase}. Exiting.")
                    sys.exit(1)

    for f_con_base in front_counts:
        best_fpair = max(f_con_base)
        if best_fpair == 0:
            add_nuc = "N"
        else:
            add_nuc = BASE_MAP[f_con_base.index(best_fpair)]
        f_con_seq = f_con_seq + add_nuc

    for b_con_base in back_counts:
        best_bpair = max(b_con_base)
        if best_bpair == 0:
            add_nuc = "N"
        else:
            add_nuc = BASE_MAP[b_con_base.index(best_bpair)]
        b_con_seq = b_con_seq + add_nuc

    final_seq = f_con_seq[::-1] + b_con_seq

    print(f"CONSENSUS SEQ FOR {MOTIF}: {final_seq}")
