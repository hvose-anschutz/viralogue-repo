#!/usr/bin/env python3

"""Takes in a list of parsed fastas and determines the most conserved region.
MISSING: Ability to find start point, handling duplicates, and handling "false" positives"""

from suffix_trees import STree
#This is the initial version

my_reads = []
pol_family = "L1"

with open("all_pol_fastas.txt","r",encoding="utf-8") as f:
    for line in f.readlines():
        my_line = line.strip().split("\t")
        if my_line[1] == pol_family:
            my_reads.append(my_line[3])
f.close()

print(f"total number of family reads: {len(my_reads)}")

#0 is the start, 1 is the end
GRAPH = {}
my_set = set()
K = 20

# just parsing the k-mers into count dict to find highest count of exact matches
for read in my_reads:
    READ_LENGTH = len(read)
    dupe_count = 0
    for i in range(READ_LENGTH-K+1):
        k_mer = read[i:i+K]
        if k_mer not in my_set:
            my_set.add(k_mer)
    for kmer in my_set:
        if kmer not in GRAPH:
            GRAPH[kmer] = 1
        else:
            GRAPH[kmer] += 1
    my_set = set()

sorted_graph = dict(sorted(GRAPH.items(), key=lambda item: item[1], reverse=True))

for key,value in sorted_graph.items():
    if value > 5900:
        print(f"key: {key}\ncount: {value}\n")


# #generating the graph by looking for an overlap of k-1
# for read in my_reads:
#     READ_LENGTH = len(read)
#     for i in range(READ_LENGTH-K+1):
#         k_mer = read[i:i+K]
#         #print(f"processing kmer {k_mer} with a range of {i} to {i+K}")
#         if k_mer not in GRAPH:
#             if i + K == READ_LENGTH:
#                 GRAPH[k_mer] = []
#             else:
#                 next_k_mer = read[i+1:i+K+1]
#                 GRAPH[k_mer] = [next_k_mer]
#         else:
#             if i + K != READ_LENGTH:
#                 next_k_mer = read[i+1:i+K+1]
#                 #need to check for duplicate anchors
#                 GRAPH[k_mer].append(next_k_mer)

#print(GRAPH)

#processing the graph to find the most conserved path

# stitching = True
# highest_count = 0
# start_point = ""
# conserved = ""
# all_longest = [] 
# for keys, values in GRAPH.items():
#     #here, we pick a starting point that meets the criteria of (len(values) = len(my_reads)) && (len(set(values)) = 1)
#     if (len(values) > highest_count) and (len(set(values)) == 1):
#         start_point = keys
#         highest_count = len(values)

# print(f"starting point of {start_point} with {highest_count} edges, which is excluding {len(my_reads)-highest_count} reads.")

# conserved = start_point[0:1]

# print("STARTING STITCH")

# while stitching:
#     #assign the next key in the graph (index doesn't matter because they all point to the same node)
#     if len(GRAPH[start_point]) < 1:
#         # we found the end
#         stitching = False
#         conserved = conserved + start_point[1:]
#     else:
#         next_key = GRAPH[start_point][0]

#         #check to see if the next node follows the rules
#         if (len(set(GRAPH[next_key])) > 1):
#             #we assume no errors, and therefore this is the end of the stitch
#             conserved = conserved + next_key
#             stitching = False
#             print("end of stitch")
#         else:
#             #the stitching continues, but we need to check for a duplicate node
#             conserved = conserved + next_key[0:1]
#             start_point = next_key

# print(conserved)