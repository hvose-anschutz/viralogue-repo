#!/usr/bin/env python3

"""The big document combining all of my utilies that I've written
as separate files. Also known as an attempt to make my documentation
more streamlined."""

import re
import sys

#EUTILS FUNCTIONALITY

def get_eutils():

    """Accesses the NCBI eutils API."""
    #ORIGINAL SCRIPT: chr_locator.py and viral_genera_finder.py

    return None

def gtf_fixer(old_file:str,output:str) -> None:

    """Fixes gtf files by adding the chr prefix for STAR."""

    with open(old_file,"r",encoding="utf-8") as f, open(output,"w",encoding="utf-8") as w:
        for line in f.readlines():
            good_stuff = []
            split_line = line.split("\t")
            for i in range(0,5):
                item = split_line[i]
                if i == 1:
                    item = "chr" + split_line[i]
                good_stuff.append(item)
            for attr in good_stuff:
                w.write(attr + "\t")
            w.write("\n")
    f.close()
    w.close()

    return None

def write_out(my_filename: str,
              item_list: list,
              delimiter: str="\n"):
    
    """Writes out a provided list to a specified file."""

    with open(my_filename,"w",encoding="utf-8") as f:
        for item in item_list:
            f.write(item + delimiter)
        f.close()

    return None

def text_to_fasta(text_file:str, fasta_out:str):
    
    """Turns a list of sequences in txt format into a fasta file format."""

    JUST_SEQS = True

    with open(text_file,"r",encoding="utf-8") as f, open(fasta_out,"w",encoding="utf-8") as o:
        for line in f.readlines():
            my_line = line.strip().split()
            o.write(f">{my_line[0]}\n")
            if JUST_SEQS:
                o.write(f"{my_line[1]}\n")
            else:
                o.write(f"{my_line[3]}\n")
    o.close()
    f.close()

    return None