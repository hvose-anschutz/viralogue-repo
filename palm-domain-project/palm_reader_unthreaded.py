#!/usr/bin/env python3 

"""Takes in a list of sequences and extracts the palm domain from each sequence without threading."""

from multiprocessing import Pool, cpu_count
import os
import subprocess
import time


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

def protein_translator(seq, started:bool=True, speed:int=3):
    """Translates a given DNA sequence into protein, and can find the relevant codon given an AA position in the translated sequence."""
    my_sequence = seq.upper()

    longest_seq = -1
    final_prot = ""
    final_orf = -1

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

        #print(f"curr seq length is {len(my_prot_seq)} in orf {orf}")
        
        if len(my_prot_seq) > longest_seq:
            longest_seq = len(my_prot_seq)
            final_prot = my_prot_seq
            final_orf = orf

    #print(final_prot)
    #print(longest_seq)
    #print(final_orf)
    return final_prot,final_orf


STARTED = True #only set this to false if you care about starting at a start codon (and not fragments)
SPEED = 3
FAMILY = "L1"

if __name__ == "__main__":
    MY_SEQS = {}
    T_START = time.time()
    print(f"time started: {T_START}")

    with open("all_pol_fastas.txt","r",encoding="utf-8") as f:
        for line in f.readlines():
            my_line = line.strip().split()

            if my_line[1] == FAMILY:
                my_seq = my_line[3]

                translated,f_orf = protein_translator(my_seq,SPEED)

                my_title = ">" + my_line[0]

                my_cmd = [f"blastp -query known_palm.fa -subject <(echo -e \"{my_title}\n{translated}\") -outfmt 6"]    

                #print(my_cmd)

                #query is always the known_palm, subject is always the test

                try:
                    result = subprocess.Popen(my_cmd,executable="/bin/bash",text=True,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    #print(result.communicate()[0])
                    start_aa = result.communicate()[0].split("\n")[0].split("\t")[8]
                    stop_aa = result.communicate()[0].split("\n")[0].split("\t")[9]
                    #print(f"start_aa is {start_aa}")
                except subprocess.CalledProcessError as e:
                    print(f"blastp failed with error code {e.returncode}")
                    print(e.stderr)
                    #standard error
                    print(e.stdout)
                    #standard output
                except IndexError as i:
                    print(f"list index is out of range")
                    print(f"id: {my_line[0]}")
                    print(result.communicate()[0])

                #formula to find starting bp equivalent: AA# x 3 - 3 + orf
                MY_SEQS[my_line[0]] = my_seq[int(start_aa)*3-3+int(f_orf):max(len(my_seq),int(stop_aa)*3-1+int(f_orf))]
            
    output_title = FAMILY + "_palm_domains_unthread.txt"

    with open(output_title,"w",encoding="utf-8") as g:
        for keys, values in MY_SEQS.items():
            g.write(f"{keys}\t{values}\n")

    print(f"completed in time {time.time()-T_START}")

                    
