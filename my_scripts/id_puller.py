#!/usr/bin/env python3

"""Pulls barcodes from a fastq file."""

barcode = False
my_barcodes = []

with open("test2.fastq",
          "r",encoding="utf-8") as f:
    for line in f:
        print(line[0])
        if line[0] == "@":
            barcode = True
        elif barcode:
            my_barcodes.append(line[0:16])
            barcode = False
f.close()

with open("/home/hvose/sandbox/test_barcodes.txt",
          "w",encoding="utf-8") as g:
    print("made the file")
    for item in my_barcodes:
        g.write(item + "\n")
g.close()
