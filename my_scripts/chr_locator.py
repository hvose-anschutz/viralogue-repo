#!/usr/bin/env python3

import re
import requests
import xmltodict
import pprint


MM_DICT = {'chr1':'NC_000067.7','chr2':'NC_000068.8','chr3':'NC_000069.7','chr4':'NC_000070.7','chr5':'NC_000071.7','chr6':'NC_000072.7',
           'chr7':'NC_000073.7','chr8':'NC_000074.7','chr9':'NC_000075.7','chr10':'NC_000076.7','chr11':'NC_000077.7','chr12':'NC_000078.7',
           'chr13':'NC_000079.7','chr14':'NC_000080.7','chr15':'NC_000081.7','chr16':'NC_000082.7','chr17':'NC_000083.7','chr18':'NC_000084.7',
           'chr19':'NC_000085.7','chrX':'NC_000086.8','chrY':'NC_000087.8','chrM':'NC_005089.1'}

URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PARAMS = {
    'db':'nuccore',
    'id': '',
    'rettype': 'gbwithparts',
    'retmode': 'text',
    'seq_start':0,
    'seq_stop':0,
    'api_key': '4067db555f3f041968fa45e511846737ca08',
    'complexity':3
}

location_genes = {}

with open("4T1_CSO36658_SJs.txt","r") as f:
    for idx, line in enumerate(f.readlines()):
        location, count = line.strip().split("\t")
        components = re.search("(chr\d+|chr[XYM]):(\d+)-(\d+)",location)
        PARAMS['id'] = MM_DICT[components.group(1)]
        PARAMS['seq_start'] = int(components.group(2))
        PARAMS['seq_stop'] = int(components.group(3))

        response = requests.get(URL,PARAMS)

        with open("test_output.txt","wb") as f:
            f.write(response.content)
        f.close()

        curr_genes = set()
        new_gene = False
        with open("test_output.txt","r") as g:
            for b_line in g.readlines():
                gene_check = re.search("(?<!/)gene",b_line)
                if gene_check is not None:
                    new_gene = True
                
                if new_gene == True:
                    the_gene = re.search('(/gene=\")(.+)\"',b_line)
                    if the_gene is not None:
                        curr_genes.add(the_gene.group(2))
                        new_gene = False
        g.close()

        location_genes[location] = curr_genes
        print("processed index " + str(idx))

    with open("4T1_CSO36558_gene_cnts.txt","w") as h:
        for keys,values in location_genes.items():
            h.write(keys + "\t" + str(values) + "\n")
    h.close()
f.close()
            
