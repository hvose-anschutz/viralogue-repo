#!/usr/bin/env python3



with open("significant_tumor_ERVs.txt", "r") as f, open("ERV_logs.txt","w") as w:
    for my_line in f.readlines():
        line = my_line.strip().split("\t")
        #w.write(line[0] + "\t")
        for i in range(73,len(line)-2,3):
            w.write(line[i] + "\t")
        w.write("\n")
f.close()
w.close()