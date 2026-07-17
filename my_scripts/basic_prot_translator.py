#!/usr/bin/env python3

"""Only translates a given sequence into protein."""

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
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G'    # Glycine
}

translator_dict = {'sequence':[]}

def protein_translator(seq:str,
                       started:bool=True,
                       speed:int=3,
                       no_stop:bool=False):
    """Translates a given DNA sequence into protein, and can find the relevant codon 
    given an AA position in the translated sequence.\n
    ARGUMENTS
    - seq: The sequence to be translated. Must be a string.
    - started: Tells function whether or not to look for a valid start codon. Default
    is True (no start codon required).
    - speed: Dictates how quickly the program checks for amino acids. Default is
    3, but can be changed if looking for valid open reading frames quickly."""
    my_seq = seq.upper()

    #print(f"parameters are started = {started} and speed = {speed}")

    my_prot_seq = ""

    all_orf_dict = {0:0,1:1,2:2,3:0,4:1,5:2}

    for orf in range(0,6):
        if orf < 3:
            #test the forward sequence
            my_sequence = my_seq
        else:
            #test the reverse sequence
            my_sequence = my_seq[::-1]
        my_prot_seq = ""

        for i in range(all_orf_dict[orf],len(my_sequence)-speed,speed):
            curr_aa = codontab[my_sequence[i:i+3]]
            if not started:
                if curr_aa == "M":
                    my_prot_seq = my_prot_seq + curr_aa
                    started = True
                    speed = 3
            else:
                if no_stop:
                    my_prot_seq = my_prot_seq + curr_aa
                else:
                    if curr_aa != '*':
                        my_prot_seq = my_prot_seq + curr_aa
                        #print(f"added amino acid {curr_aa}")
                    else:
                        break

        translator_dict['sequence'].append(my_prot_seq)

    return translator_dict

protein_translator(sys.argv[1],no_stop=True)

for keys,values in translator_dict.items():
    for idx, aa_seq in enumerate(values):
        if "FADD" in aa_seq:
            print(f"orf {idx}: {aa_seq}")
