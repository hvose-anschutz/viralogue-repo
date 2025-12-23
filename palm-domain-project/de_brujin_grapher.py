#!/usr/bin/env python3

"""Takes in a list of parsed fastas and determines the most conserved region."""

import re

#This is the initial version

my_reads = ["ratty","batter","batty","batter","abattey"]

#0 is the start, 1 is the end
GRAPH = {}
K = 3

#generating the graph by looking for an overlap of k-1
for read in my_reads:
    READ_LENGTH = len(read)
    for i in range(READ_LENGTH-K+1):
        k_mer = read[i:i+K]
        #print(f"processing kmer {k_mer} with a range of {i} to {i+K}")
        if k_mer not in GRAPH:
            if i + K == READ_LENGTH:
                GRAPH[k_mer] = []
            else:
                next_k_mer = read[i+1:i+K+1]
                GRAPH[k_mer] = [next_k_mer]
        else:
            if i + K != READ_LENGTH:
                next_k_mer = read[i+1:i+K+1]
                #need to check for duplicate anchors
                
                GRAPH[k_mer].append(next_k_mer)

print(GRAPH)

#processing the graph to find the most conserved path

stitching = True
highest_count = 0
start_point = ""
conserved = ""
anchor = 0

for keys, values in GRAPH.items():
    #here, we pick a starting point that meets the criteria of (len(values) = len(my_reads)) && (len(set(values)) = 1)
        if len(values) > highest_count:
            start_point = keys
            highest_count = len(values)

conserved = start_point[0:1]

while stitching:
    #assign the next key in the graph (index doesn't matter because they all point to the same node)
    next_key = GRAPH[start_point][0]

    #check to see if the next node follows the rules
    if len(set(GRAPH[next_key])) > 1:
        #we assume no errors, and therefore this is the end of the stitch
        conserved = conserved + next_key
        stitching = False
    else:
        #the stitching continues, but we need to check for a duplicate node

        conserved = conserved + next_key[0:1]
        start_point = next_key

print(conserved)