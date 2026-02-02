#!/usr/env/bin python3

"""pulls all of the fasta sequences given a list of Mmus IDs"""

import re

#VALID_ERVS = ["MLV","MuRRS","MMERV","VL30","GLN","IAPE","L1"]
VALID_ERVS = ["HERVH"]
ID_KEY = None
ID_SEQ = None
MMUS_FA_DICT = {}
FILTERED_ERVS = []

VALID_NTS = 0

#0: hash the fastas
with open("Hsap38.geve.ntm_v1.fa","r",encoding="utf-8") as f:
    for line in f.readlines():
        if ID_KEY is not None:
            ID_SEQ = line.strip("M\n$")
            MMUS_FA_DICT[ID_KEY] = ID_SEQ
            ID_KEY = None
            ID_SEQ = None
        else:
            ID_KEY = line.strip()
f.close()

#1: get IDs that match "pol" in column 10 and valid ERVs in 15

with open("Hsap38.txt","r",encoding="utf-8") as g:
    for line in g.readlines():
        #print("checking line " + line)
        my_items = line.strip().split("\t")
        #print("checking " + my_items[10])
        valid_pol = re.search(f"[P|p]ol",my_items[10])
        if valid_pol is not None:
            #print("found a pol")
            #now we check for the valid ERVS
            if int(my_items[5]) > VALID_NTS:
                valid_mmtv = re.search("MMTV",my_items[14])
                valid_iap = re.search("IAP",my_items[14])
                #print("checking " + my_items[14])
                if valid_mmtv is not None:
                    #we have found a valid MMTV ERV, can put into the list to search for 
                    FILTERED_ERVS.append([my_items[0],"MMTV",my_items[5],MMUS_FA_DICT[">" + my_items[0]]])
                elif valid_iap is not None:
                    #we have found a valid IAP
                    FILTERED_ERVS.append([my_items[0],"IAP",my_items[5],MMUS_FA_DICT[">" + my_items[0]]])
                else:
                    #now we get to check all of the col 15 ERVs in VALID_ERVS
                    for erv in VALID_ERVS:
                        check_erv = re.search(erv,my_items[15])
                        if check_erv is not None:
                            #we found a valid erv
                            FILTERED_ERVS.append([my_items[0],erv,my_items[5],MMUS_FA_DICT[">" + my_items[0]]])
                            break
g.close()

with open("all_hsap_pol_fastas.txt","w",encoding="utf-8") as o:
    for lines in FILTERED_ERVS:
        o.write("\t".join(lines))
        o.write("\n")
o.close()