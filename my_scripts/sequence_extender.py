#!/usr/bin/env python3

"""A script that extends a given sequence based on the provided reference
and the coordinates. Used to find the EN domain, ORF1, and the 5'UTR of
human L1HS sequences."""

import requests

#STEP 0: Define the globals:
#  ID dictionary to pull efetch accession numbers
#  master dict to catch all of the request results

HG_ACCESSION = {"chr1":"NC_000001.11","chr2":"NC_000002.12","chr3":"NC_000003.12",
                "chr4":"NC_000004.12","chr5":"NC_000005.10","chr6":"NC_000006.12",
                "chr7":"NC_000007.14","chr8":"NC_000008.11","chr9":"NC_000009.12",
                "chr10":"NC_000010.11","chr11":"NC_000011.10","chr12":"NC_000012.12",
                "chr13":"NC_000013.11","chr14":"NC_000014.9","chr15":"NC_000015.10",
                "chr16":"NC_000016.10","chr17":"NC_000017.11","chr18":"NC_000018.10",
                "chr19":"NC_000019.10","chr20":"NC_000020.11","chr21":"NC_000021.9",
                "chr22":"NC_000022.11","chrX":"NC_000023.11","chrY":"NC_000024.10"}

EXTENDED_SEQS = {}

#STEP 1: Parse the sequence document

with open("../my_data/all_L1HS_RT_coords.txt","r",encoding="utf-8") as f:
    for idx, line in enumerate(f.readlines()):
        my_line = line.strip().split("\t")
        ref,chr_num,start,stop,strand = my_line[0].strip().split(".")
        match strand:
            case "+":
                strand=1
                startadd=3303
                endadd=208
            case "-":
                strand=2
                startadd=208
                endadd=3303

        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            'db':'nuccore',
            'id': HG_ACCESSION[chr_num],
            'rettype':'fasta',
            'retmode':'text',
            'seq_start':str(int(start)-startadd),
            'seq_stop':str(int(stop)+endadd),
            'strand':strand,
            'api_key':'4067db555f3f041968fa45e511846737ca08',
            'complexity':3
        }

        response = requests.get(url,params,timeout=10)

        EXTENDED_SEQS[my_line[0]] = response.text.split("\n",1)[1].replace("\n","")

f.close()

with open("all_L1HS_extended_seqs.fa","w",encoding="utf-8") as out:
    for keys,vals in EXTENDED_SEQS.items():
        out.write(f">{keys}\n{vals}\n")
out.close()

