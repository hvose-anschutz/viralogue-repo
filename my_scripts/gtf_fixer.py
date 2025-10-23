#!/usr/bin/env python3

with open("Mmus38.gtf.txt", "r") as f, open("Mmus38_ERV.gtf","w") as w:
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
