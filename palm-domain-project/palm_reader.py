#!/usr/bin/env python3 

"""Takes in a list of sequences and extracts the known palm domain from each sequence."""

from multiprocessing import Pool, cpu_count
import subprocess
import sys
import time

codontab = {
    'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S', 'AGC': 'S', 'AGT': 'S',
    'TTC': 'F', 'TTT': 'F',
    'TTA': 'L', 'TTG': 'L', 'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
    'TAC': 'Y', 'TAT': 'Y',
    'TAA': '*', 'TAG': '*', 'TGA': '*',
    'TGC': 'C', 'TGT': 'C',
    'TGG': 'W',
    'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
    'CAC': 'H', 'CAT': 'H',
    'CAA': 'Q', 'CAG': 'Q',
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R', 'AGA': 'R', 'AGG': 'R',
    'ATA': 'I', 'ATC': 'I', 'ATT': 'I',
    'ATG': 'M',
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
    'AAC': 'N', 'AAT': 'N',
    'AAA': 'K', 'AAG': 'K',
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
    'GAC': 'D', 'GAT': 'D',
    'GAA': 'E', 'GAG': 'E',
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G'
}

def protein_translator(seq, started:bool=True, speed:int=3):
    """Translates a given DNA sequence into protein, and can find the relevant codon 
    given an AA position in the translated sequence."""
    my_sequence = seq.upper()

    longest_seq = -1
    final_prot = ""
    final_orf = -1

    for orf in range(0,3):
        my_prot_seq = ""
        for i in range(orf,len(my_sequence)-3,speed):
            curr_AA = codontab[my_sequence[i:i+3]]
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
        
        if len(my_prot_seq) > longest_seq:
            longest_seq = len(my_prot_seq)
            final_prot = my_prot_seq
            final_orf = orf

    return final_prot,final_orf

def process_line(line:str):
    """Takes in a line from a list of files and generates a `blastp` query based on the formatting.
    Returns the specific ERV ID and the chunk of the string that matches the known fasta sequence."""
    #my_line = line.strip().split()
    my_line = line.strip().split("\t")
    print(f"my line is {my_line}")
    print(f"my_line[0] is {my_line[0]} and my_line[1] is {my_line[1]}")

    known_palm = "known_" + FAMILY + "_palm.fa"
    #if my_line[1] == FAMILY:
    if my_line[0][0] == ">":
        my_title = my_line[0]
        my_seq = my_line[1]
        #my_seq = my_line[3]

        translated,f_orf = protein_translator(my_seq,SPEED)

        #my_title = ">" + my_line[0]

        my_cmd = [f"""blastp -query known_HERVH_palm.fa -subject <(echo -e \"{my_title}\n{translated}\") -outfmt 6"""]    

        try:
            result = subprocess.Popen(my_cmd,
                                      executable="/bin/bash",
                                      text=True,
                                      shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            #print(result.communicate()[0])
            my_result = result.communicate()[0].split("\n")[0].split("\t")
            if len(my_result) < 2:
                return ["ERROR","ERROR","ERROR","ERROR"]
            else:
                percent_sim = my_result[2]
                e_value = my_result[10]
                start_aa = my_result[8]
                stop_aa = my_result[9]
                #if float(percent_sim) >= float(40.000):
                return [my_line[0],
                        percent_sim,
                        e_value,
                        my_seq[int(start_aa)*3-3+int(f_orf):max(len(my_seq),int(stop_aa)*3-1+int(f_orf))]]
                # else:
                #     return
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
            print(result.communicate())

        #formula to find starting bp equivalent: AA# x 3 - 3 + orf
    else:
        return

def process_file(filename:str, output_filename: str, start: float):
    results = []
    with open(filename, "r", encoding="utf-8") as foo:
        with Pool(cpu_count()) as pool:
            for result in pool.imap(process_line,foo,chunksize=500):
                if result is not None:
                    results.append(result)
                if len(results) % 1000 == 0:
                    print(f"stored {len(results)} items at time {time.time()-start}")

    for all_palms in results:
        MY_SEQS[all_palms[0]] = [all_palms[1],all_palms[2],all_palms[3]]

    with open(output_filename, 'w', encoding='utf-8') as out:
        for keys,values in MY_SEQS.items():
            out.write(f"{keys}\t{' '.join(values)}\n")
    out.close()

STARTED = True #only set this to false if you care about starting at a start codon (and not fragments)
SPEED = 3
FAMILY = "IAP"

if __name__ == "__main__":
    MY_SEQS = {}
    T_START = time.time()
    print(f"time started: {T_START}")
    process_file("untranslated_HERVH.txt","HERVH_palms.txt",T_START)
    print(f"completed in time {time.time()-T_START}")          

