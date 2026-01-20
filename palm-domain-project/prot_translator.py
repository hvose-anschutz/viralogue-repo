#!/usr/bin/env python3 

"""Translates a given DNA sequence into protein, and can find the relevant codon given an AA position in the translated sequence."""

codontab = {
    'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',    # Serine
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
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',    # Arginine
    'ATA': 'I', 'ATC': 'I', 'ATT': 'I',    # Isoleucine
    'ATG': 'M',    # Methionine
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',    # Threonine
    'AAC': 'N', 'AAT': 'N',    # Asparagine
    'AAA': 'K', 'AAG': 'K',    # Lysine
    'AGC': 'S', 'AGT': 'S',    # Serine
    'AGA': 'R', 'AGG': 'R',    # Arginine
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',    # Valine
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',    # Alanine
    'GAC': 'D', 'GAT': 'D',    # Aspartic Acid
    'GAA': 'E', 'GAG': 'E',    # Glutamic Acid
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G'     # Glycine
}

with open("all_pol_fastas.txt","r",encoding="utf-8") as f:
    for line in f.readlines():
        my_line = line.strip().split()
        

my_seq = "ctacacaaacaagacccaacattttgctgtttacaggagacacatctcagagaaaaagatagacactacctcagaataaaaggctggaaaacaattttccgagcaaatggtatgaagaaacaagctggagtagccatcctaatatctgataagattgacttccaacccaaagtaatcaaaaaagacaaggaggggcacttcgttctcatcaaaggtaaaatcctccaagaggaactctcaattctgaatatctatgctccaaatacaagggcagccacattcactcaagaaactttagtaacgctcaaagcacacattgcacctcacacaataatagtgggagacttcaacacaccactttcaccaatggacagatcatggaaacagaaactaaacagggacacactgaaactaacagaagtgatgaaacaaatggatctgacagatatctacagaacattttatcctaaaacaaaaggatataccttcttctcagcacctcatggtaccttctccaaaattgaccacataataggtcacaaaacaggcctcaacagattcaaaaatattgaaattgtcccatgtatcctatcagatcaccatgcactaaggctgatcttcaataacaaaaaaaataacagaaagccaacactcacgtggaaactgaacaacactcttctcaatgataccttggtcaaggaaggaataaagaaagaaattaaagactttttagagtttaatgaaaatgaagccacaacgtacccaaaactttgggacacaaagaaagcatttctaagagggaaactcatagctctgagtgcctccaagaagaaacgggagagagcacatactagcagcttgacaacacatctaaaagctctagaaaaaaaggaagcaaattcacccaagaggagtagagggcaggaaataatcaaactcaggggtgaaatcaaccaagtggaaacaagaagaactattcaaagaattaaccaaacgaggagttggttctttgagaaaatcaacaagatagataaacccttagctagactcactagagggcacagagacaaaatcctaattaacaaaatcagaactgaaaagggagacataacaacagatcctgaagaaatccaaaacaccatcagatccttctacaaaaggctatactcaacaaaactggaaaacctggacgaaatggacaaatttctggacagataccaggtaccaaagttgaatcaggatcaagttgaccttctaaacagtcccatatcccctaaagaaatagaagcagttataaatagtctcccagccaaaaaaagcccaggaccagacgggtttagtgcagagttctatcagaccttcaaagaagatctaattccagttctgcacaaactttttcacaagatagaagtagaaagtactctacccaactcattttatgaagccactattactctgatacctaaaccacagaaagatccaacaaagatagagaacttcagaccaatttctcttatgaatatcgatgcaaaaatcctcaataaaattctcgctaaccgaatccaagaacacattaaagcaatcatccatcctgaccaagtaggttttattccagggatgcagggatggtttaatatacgaaaatccatcaatgtaatccactatataaacaaactcaaagacaaaaaacacatgatcatctcgttagatgcagaaaaagcatttgacaagatccaacacccattcatgataaaagttctggaaagatcaggaattcaaggcccatacctaaacatgataaaagcaatctacagcaaaccaggagccaacatcaaagtaaatggagagaagctggaagcaatcccactaaaatcagggactagacaaggctgcccactttctccctaccttttcaacatagtacttgaagtattagccagagcaattcgacaacaaaaggagatcaaggggatacaaattggaaaagaggaaatcaaaatatcactttttgcagatgatatgatagtatatataagtgaccctaaaaattccaccagagaactcctaaacctgataaacagcttcggtgaagaagctggatataaaattaactcaaacaagtcaatggcctttctctacacaaagaataaacaggctgagaaagaaattagggaaacaacacccttctcaatagtcacaaataatataaaatatctcggagtgactctaactaaggaagtgaaagatctgtatgataaaaacttcaagtctctgaagaaagaaattaaagaagatctcagaagatggaaagatctcccatgctcatggattggcaggatcaacattgtaaaaatggctatcttgccaaaagcaatctacagattcaatgcaatccccatcaaaattccaactcaattcttcaatgaattagaaggagcaatttgcaaattcatctggaataacaaaaacctagga"
started = True
speed = 3
longest_seq = -1
final_prot = ""
final_orf = -1

#formula to find starting bp equivalent is AA# x 3 - 3 + orf
print(my_seq[2214:2217])

my_sequence = my_seq.upper()

for orf in range(0,3):
    my_prot_seq = ""
    for i in range(orf,len(my_sequence)-3,speed):
        curr_AA = codontab[my_sequence[i:i+3]]
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

    print(f"curr seq length is {len(my_prot_seq)} in orf {orf}")
    
    if len(my_prot_seq) > longest_seq:
        longest_seq = len(my_prot_seq)
        final_prot = my_prot_seq
        final_orf = orf

print(final_prot)
print(longest_seq)
print(final_orf)

