#!/usr/bin/env python3

"""Takes in a list of parsed fastas and determines the most conserved region."""

#This is the initial version

my_reads = ["batty","batter","ratty","ratter"]

#0 is the start, 1 is the end
GRAPH = {0:[]}
K = 3

#generating the graph by looking for an overlap of k-1
for read in my_reads:
    READ_LENGTH = len(read)
    for i in range(READ_LENGTH-K+1):
        k_mer = read[i:i+K]
        #print(f"processing kmer {k_mer} with a range of {i} to {i+K}")
        if i == 0:
            GRAPH[0].append(k_mer)
        if k_mer not in GRAPH:
            if i + K == READ_LENGTH:
                GRAPH[k_mer] = [1]
            else:
                next_k_mer = read[i+1:i+K+1]
                GRAPH[k_mer] = [next_k_mer]
        else:
            if i + K == READ_LENGTH:
                GRAPH[k_mer].append(1)
            else:
                next_k_mer = read[i+1:i+K+1]
                GRAPH[k_mer].append(next_k_mer)

print(GRAPH)

#processing the graph to find the most conserved path

stitching = True
next_check = 0
prev_high = 0
most_nodes = 0
conserved = ""

