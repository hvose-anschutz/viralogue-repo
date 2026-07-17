#!/usr/bin/env python3

"""Translates a fasta file into protein. Expects an ID-sequence pair."""

import re
import sys
import txt_to_fa

SINGLE_LINE = False

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
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G'    # Glycine
}

def translator(my_sequence:str,
             orf:int,
             started:bool,
             stop:bool) -> str:
    """Translates a protein sequence.
    - my_sequence: nucleotide sequence to be translated.
    - orf: open reading frame to use.
    - started: flag to use valid start codons.
    - stop: flag to use stop codons"""
    my_prot_seq = ""
    for i in range(orf,len(my_sequence)-3,3):
        curr_aa = codontab[my_sequence[i:i+3]]
        if not started:
            if curr_aa == "M":
                my_prot_seq = my_prot_seq + curr_aa
                started = True
        my_prot_seq = my_prot_seq + curr_aa
        if stop:
            if curr_aa == '*':
                return my_prot_seq
                #print(f"added amino acid {curr_aa}")
    return my_prot_seq

def protein_checker(seq:str,
                    started:bool=False,
                    stop:bool=False,
                    confirm_seq:str="",
                    specify_orf:int|None=None) -> tuple[list,list]:
    """Translates a given DNA sequence into protein, and can find the relevant codon 
    given an AA position in the translated sequence.\n
    ARGUMENTS
    - seq: The sequence to be translated. Must be a string.
    - started: Tells function whether or not to look for a valid start codon. Default
    is True (no start codon required).
    - stop: determines if the program should look for a valid stop codon.
    Default is False (will not look for valid stop codons.)
    - confirm_seq: Regex sequence to check the amino acid sequence for.
    - specify_orf: Use a specific orf instead of checking all orfs"""
    orf_list = []
    translator_list = []

    if specify_orf is not None:
        return [translator(seq.upper(),specify_orf,started,stop)], [specify_orf]
    
    for orf in range(0,3):
        forward = translator(seq.upper(),orf,started,stop)
        backward = translator(seq.upper()[::-1],orf,started,stop)
        if confirm_seq != "":
            if re.search(confirm_seq, forward) is not None:
                translator_list.append(forward)
                orf_list.append(orf)
            if re.search(confirm_seq, backward) is not None:
                translator_list.append(backward)
                orf_list.append(orf*-1)
        else:
            translator_list.append(forward)
            translator_list.append(backward)
            orf_list.append(orf)
            orf_list.append(orf*-1)

    return translator_list, orf_list

#print(translator_dict)

translated_seqs = {}

with open(sys.argv[1],
          "r",
          encoding="utf-8") as f, open("translated_fasta_full.fa",
                                       "w",
                                       encoding="utf-8") as out:
    for line in f.readlines():
        if not SINGLE_LINE:
            if line[0] == ">":
                curr_id = line
                #print(f"curr id = {curr_id}")
            else:
                results,orfs = protein_checker(line.replace("\n",""),
                                               stop=True,
                                               confirm_seq="FADD")
                for idx, val in enumerate(results):
                    out.write(f"{curr_id.strip()}_orf{orfs[idx]}\n")
                    out.write(f"{val}\n")
        else:
            my_line = line.strip().split()
            curr_id = my_line[0]
            results,orfs = protein_checker(my_line[1].replace("\n",""),
                                           stop=False,
                                           confirm_seq="FADD")
            for idx, val in enumerate(results):
                out.write(f"{curr_id.strip()}_orf{orfs[idx]}\n")
                out.write(f"{val}\n")
f.close()
out.close()
