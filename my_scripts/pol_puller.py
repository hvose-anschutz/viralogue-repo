#!/usr/env/bin python3

"""Pulls all of the fasta sequences given a list of Mmus IDs"""

#regex for pol: [P|p]ol in line 33

import re

VALID_ERVS = ["L1HS"]
ID_KEY = None
ID_SEQ = None
MMUS_FA_DICT = {}
FILTERED_ERVS = []

#0: hash the fastas
with open("Hsap38.geve.nt_v1.fa","r",encoding="utf-8") as f:
    for line in f.readlines():
        if ID_KEY is not None:
            ID_SEQ = line.strip()
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
        valid_pol = re.search("RVT|RT",my_items[10])
        if valid_pol is not None:
            #print("found a pol")
            #now we check for the valid ERVS
            if int(my_items[5]) >= 1000:
                #valid_mmtv = re.search("MMTV",my_items[14])
                #valid_iap = re.search("IAP",my_items[14])
                #print("checking " + my_items[14])
                #if valid_mmtv is not None:
                #    #we have found a valid MMTV ERV, can put into the list to search for
                #    FILTERED_ERVS.append([my_items[0],
                #                          "MMTV",
                #                          my_items[5],
                #                          MMUS_FA_DICT[">" + my_items[0]]])
                #elif valid_iap is not None:
                #    #we have found a valid IAP
                #    FILTERED_ERVS.append([my_items[0],
                #                          "IAP",
                #                          my_items[5],
                #                          MMUS_FA_DICT[">" + my_items[0]]])
                    #now we get to check all of the col 15 ERVs in VALID_ERVS
                for erv in VALID_ERVS:
                    check_erv = re.search(erv,my_items[15])
                    if check_erv is not None:
                        #we found a valid erv
                        FILTERED_ERVS.append([my_items[0],
                                            erv,
                                            my_items[5],
                                            MMUS_FA_DICT[">" + my_items[0]]])
                        break
g.close()

#2: write the information to a text file
with open("all_L1HS_RT_coords.txt","w",encoding="utf-8") as o:
    for lines in FILTERED_ERVS:
        o.write("\t".join(lines))
        o.write("\n")
o.close()
