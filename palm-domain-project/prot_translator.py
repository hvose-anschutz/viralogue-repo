#!/usr/bin/env python3

"""Translates nucleotides into protein."""

import sys

codontab = {
    'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S', 'AGC': 'S', 'AGT': 'S',   # Serine
    'TTC': 'F', 'TTT': 'F',    # Phenylalanine
    'TTA': 'L', 'TTG': 'L',    # Leucine
    'TAC': 'Y', 'TAT': 'Y',    # Tyrosine
    'TAA': '*', 'TAG': '*', 'TGA': '*',    # Stop
    'TGC': 'C', 'TGT': 'C',    # Cysteine
    'TGG': 'W',    # Tryptophan
    'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',    # Leucine
    'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',    # Proline
    'CAC': 'H', 'CAT': 'H',    # Histidine
    'CAA': 'Q', 'CAG': 'Q',    # Glutamine
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R', 'AGA': 'R', 'AGG': 'R',  # Arginine
    'ATA': 'I', 'ATC': 'I', 'ATT': 'I',    # Isoleucine
    'ATG': 'M',    # Methionine
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',    # Threonine
    'AAC': 'N', 'AAT': 'N',    # Asparagine
    'AAA': 'K', 'AAG': 'K',    # Lysine
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',    # Valine
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',    # Alanine
    'GAC': 'D', 'GAT': 'D',    # Aspartic Acid
    'GAA': 'E', 'GAG': 'E',    # Glutamic Acid
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G'     # Glycine
}

def protein_translator(seq: str, started:bool=True, speed:int=3, all_orfs:bool=False):
    """Translates a given DNA sequence into protein, and can find the relevant codon 
    given an AA position in the translated sequence.\n
    ARGUMENTS
    - seq: The sequence to be translated. Must be a string.
    - started: Tells function whether or not to look for a valid start codon. Default
    is True (no start codon required).
    - speed: Dictates how quickly the program checks for amino acids. Default is
    3, but can be changed if looking for valid open reading frames quickly."""
    my_sequence = seq.upper()

    print(f"parameters are started = {started} and speed = {speed}")

    longest_seq = -1
    final_prot = ""
    final_orf = -1
    my_prot_seq = ""

    for orf in range(0,3):
        my_prot_seq = ""
        for i in range(orf,len(my_sequence)-speed,speed):
            curr_AA = codontab[my_sequence[i:i+3]]
            #print(f"curr_AA is {curr_AA}")
            #print(f"curr AA is {curr_AA}")
            if not started:
                if curr_AA == "M":
                    my_prot_seq = my_prot_seq + curr_AA
                    started = True
                    speed = 3
            else:
                if curr_AA != '*':
                    my_prot_seq = my_prot_seq + curr_AA
                else:
                    break
                #my_prot_seq = my_prot_seq + curr_AA

            print(f"current ORF: {orf}\ncurrent seq: {my_prot_seq}")

        #print(f"curr seq length is {len(my_prot_seq)} in orf {orf}")
        if "DD" in my_prot_seq:
            if len(my_prot_seq) > longest_seq:
                longest_seq = len(my_prot_seq)
                final_prot = my_prot_seq
                final_orf = orf

    return final_prot,final_orf

prot_seq = None
title = None
all_prots = {}

with open(sys.argv[1], "r", encoding="utf-8") as f:
    print("started work")
    for line in f.readlines():
        if line[0] != ">":
            prot_seq = protein_translator(line.strip(),all_orfs=True)
        else:
            title = line
        
        if (prot_seq is not None) and (title is not None):
            all_prots[title] = prot_seq
            prot_seq = None
            title = None
f.close()

with open("All_HERVH_proteins.fa", "w",encoding="utf-8") as g:
    for key, values in all_prots.items():
        g.write(f"{key}{values}\n")
g.close()

