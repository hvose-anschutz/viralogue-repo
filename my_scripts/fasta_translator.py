#!/usr/bin/env python3

"""Translates a fasta file into protein. Expects an ID-sequence pair."""

import re
import sys

#my_seq = 'gcaaaatcaccagctaacatcataatgacaggatcaaattcacacataacaatattaactttaaatataaatggactaaattctgcaattaaaagacacagacgggcaagttggataaagagccaagacccatcagtgtgctgtattcaggaaacccatctcacgtgcagagacacacacaggctcaaaataaaaggatggaggaagatctaccaagccaatggaaaacaaaaaaaggcaggggttgcaatcctagtctctgataaaacagactttaaaccaacaaagatcaaaagagacaaagaaggccattacataatggtaaagggatcaattcaacaagaggagctaactatcctaaatatttatgcacccaatacaggagcacccagattcataaagcaagtcctgagtgacctacaaagagacttagactcccacacattaataatgggagactttaacaccccactgtcaacattagacagatcaacgagacagaaagtcaacaaggatacccaggaattgaactcagctctgcaccaagcagacctaatagacatctacagaactctccaccccaaatcaacagaatatacatttttttcagcaccacaccacacctattccaaaattgaccacatagttggaagtaaagctctcctcagcaaatgtaaaagaacagaaattataacaaactatctctcagaccacagtgcaatcaaactagaactcaggattaagaatctcactcaaagccgctcaactacatggaaactgaacaacctgctcctgaatgactactgggtacataacgaaatgaaggcagaaataaagatgttctttgaaaccaacgagaacaaagacaccacataccagaatctctgggacgcattcaaagcagtgtgtagagggaaatttatagcactaaatgcctacaagagaaagcaggaaagatccaaaattgacaccctaacatcacaattaaaagaactagaaaagcaagagcaaacacattcaaaagctagcagaaggcaagaaataactaaaatcagagcagaactgaaggaaatagagacacaaaaaacccttcaaaaaatcaatgaatccaggagctggttttttgaaaggatcaacaaaattgatagaccgctagcaagactaataaagaaaaaaagagagaagaatcaaatagacacaataaaaaatgataaaggggatatcaccaccgatcccacagaaatacaaactaccatcagagaatactacaaacacctctacgcaaataaactagaaaatctagaagaaatggatacattcctcgacacatacactctcccaagactaaaccaggaagaagttgaatctctgaatagaccaataacaggctctgaaattgtggcaataatcaatagtttaccaaccaaaaagagtccaggaccagatggattcacagccgaattctaccagaggtacaaggaggaactggtaccattccttctgaaactattccaatcaatagaaaaagagggaatcctccctaactcattttatgaggccagcatcattctgataccaaagcagggcagagacacaaccaaaaaagagaattttagaccaatatccttgatgaacattgatgcaaaaatcctcaataaaatactggcaaaccaaatccagcagcacatcaaaaagcttatccaccatgatcaagtgggcttcatccctgggatgcaaggctggttcaatatacgcaaatcaataaatgtaatccagcatataaacagagccaaagacaaaaaccacatgattatctcaatagatgcagaaaaagcctttgacaaaattcaacaacccttcatgctaaaaactctcaataaattaggtattgatgggacgtatttcaaaataataagagctatctatgacaaacccacagccaatatcatactgaatgggcaaaaactggaagcattccctttgaaaaccggcacaagacaagaatgccctctctcaccgctcctattcaacatagtgttggaagttctggccagggcaatcaggcaggagaaggaaataaagggtattcaattaggaaaagaggaagtcaaattgtccctgtttgcagacaacatgattgtttatctagaaaaccccatcgtctcagcccaaaatctccttaagctgataagcaacttcagcaaagtctcaggctacaaaatcaatgtacaaaaatcacaagcattcttatacaccaacaacagacaaacagagagccaaatcatgagtgaactcccattcacaattgcttcaaagagaataaaatacctaggaatcccacttacaagggatgtgaaggacctcttcaaggagaactacaaaccactgctcaaggaaataaaagaggacacaaacaaatggaagaacattccatgctcatgggtaggaagaatcaatatcgtgaaaatggccatactgcccaaggtaatttacagattcaatgccatccccatcaagctaccaatgactttcttcacagaattggaaaaaactactttaaagttcatatggaaccaaaaaagagcccgcatcgccaagtcaatcctaagccaaaagaacaaagctggaggcatcacactacctgacttcaaactatactacaaggctacagtaaccaaaacagcatggtactggtaccaaaacagagatatagatcaatggaacagaacagagccctcagaaataatgccacatatctacaactatctgatctttgacaaacctgagaaaaacaagcaatggggaaaggattccctatttaataaatggtgctgggaaaactggctagccatatgtagaaagctgaaactggatcccttccttacaccttatacaaaaatcaattcaagatggattaaagatttaaacgttagacctaaaaccataaaaaccctagaagaaaacctaggcattaccattcaggacataggcgtgggcaaggacttcatgtccaaaacaccaaaagcaatggcaacaaaagccaaaattgacaaatgggatctaattaaactaaagagcttctgcacagcaaaagaaactaccatcagagtgaacaggcaacctacaacatgggagaaaattttcgcaacctactcatctgacaaagggctaatatccagaatctacaatgaactcaaacaaatttacaagaaaaaaacaaacaaccccatcaaaaagtgggcgaaggacatgaacagacacttctcaaaagaagacatttatgcagccaaaaaacacatgaagaaatgctcatcatcactggccatcagagaaatgcaaatcaaaaccactatgagatatcatctcacaccagttagaatggcaatcattaaaaagtcaggaaacaacaggtgctggagaggatgtggagaaataggaacacttttacactgttggtgggactgtaaactagttcaaccattgtggaagtcagtgtggcgattcctcagggatctagaactagaaataccatttgacccagccatcccattactgggtatatacccaaaggactataaatcatgctgctataaagacacatgcacacgtatgtttattgcggcactattcacaacagcaaagacttggaaccaacccaaatgtccaacaatgatagactggattaagaaaatgtggcacatatacaccatggaatactatgcagccataaaaaatgatgagttcatgtcctttgtagggacatggatgaaattggaaaccatcattctcagtaaactatcgcaagaacaaaaaaccaaacaccgcatattctcactcataggtgggaac'
single_line = False

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

def protein_translator(seq:str,
                       started:bool=True,
                       speed:int=3,
                       no_stop:bool=False,
                       confirm_seq:str="",
                       specify_orf:int|None=None):
    """Translates a given DNA sequence into protein, and can find the relevant codon 
    given an AA position in the translated sequence.\n
    ARGUMENTS
    - seq: The sequence to be translated. Must be a string.
    - started: Tells function whether or not to look for a valid start codon. Default
    is True (no start codon required).
    - speed: Dictates how quickly the program checks for amino acids. Default is
    3, but can be changed if looking for valid open reading frames quickly."""
    my_seq = seq.upper()

    translator_list = []
    orf_list = []

    #print(f"parameters are started = {started} and speed = {speed}")

    my_prot_seq = ""

    all_orf_dict = {0:0,1:1,2:2,3:0,4:1,5:2}

    if specify_orf is not None:
        for i in range(all_orf_dict[orf],len(my_sequence)-speed,speed):
            curr_AA = codontab[my_sequence[i:i+3]]
            if not started:
                if curr_AA == "M":
                    my_prot_seq = my_prot_seq + curr_AA
                    started = True
                    speed = 3
            else:
                if no_stop:
                    my_prot_seq = my_prot_seq + curr_AA
                else:
                    if curr_AA != '*':
                        my_prot_seq = my_prot_seq + curr_AA
                        #print(f"added amino acid {curr_AA}")
                    else:
                        break
        if confirm_seq != "":
            seq_check = re.search(confirm_seq,my_prot_seq)
            if seq_check is not None:
                translator_list.append(my_prot_seq)
            else:
                translator_list.append(f"NO VALID SEQ (missing {confirm_seq})")
        else:
            translator_list.append(my_prot_seq)
    else:
        for orf in range(0,6):
            if orf < 3:
                #test the forward sequence
                my_sequence = my_seq
            else:
                #test the reverse sequence
                my_sequence = my_seq[::-1]
            my_prot_seq = ""

            for i in range(all_orf_dict[orf],len(my_sequence)-speed,speed):
                curr_AA = codontab[my_sequence[i:i+3]]
                if not started:
                    if curr_AA == "M":
                        my_prot_seq = my_prot_seq + curr_AA
                        started = True
                        speed = 3
                else:
                    if no_stop:
                        my_prot_seq = my_prot_seq + curr_AA
                    else:
                        if curr_AA != '*':
                            my_prot_seq = my_prot_seq + curr_AA
                            #print(f"added amino acid {curr_AA}")
                        else:
                            break
            #print(my_prot_seq)
            if confirm_seq != "":
                seq_check = re.search(confirm_seq, my_prot_seq[50:])
                #print(seq_check)
                if seq_check is not None:
                    #print(f"using orf {orf}")
                    translator_list.append(my_prot_seq)
                    orf_list.append(orf)
            else:
                translator_list.append(my_prot_seq)
                orf_list.append(orf)
    
    return translator_list, orf_list


#print(translator_dict)

translated_seqs = {}

with open(sys.argv[1],"r",encoding="utf-8") as f, open("translated_fasta_full.fa", "w", encoding="utf-8") as out:
    for line in f.readlines():
        if not single_line:
            if line[0] == ">":
                curr_id = line
                #print(f"curr id = {curr_id}")
            else:
                results,orfs = protein_translator(line.replace("\n",""),no_stop=True,confirm_seq="FADD")
                for idx, val in enumerate(results):
                    out.write(f"{curr_id.strip()}_orf{orfs[idx]}\n")
                    out.write(f"{val}\n")
        else:
            my_line = line.strip().split()
            curr_id = my_line[0]
            results,orfs = protein_translator(my_line[1].replace("\n",""),no_stop=True,confirm_seq="FADD")
            for idx, val in enumerate(results):
                out.write(f"{curr_id.strip()}_orf{orfs[idx]}\n")
                out.write(f"{val}\n")
        

f.close()
out.close()




