#!/usr/bin/env python3

barcode = False
my_barcodes = []

with open("test2.fastq","r") as f:
    print("file opened")
    for line in f:
        print(line[0])
        if line[0] == "@":
            print('match')
            barcode = True
        elif barcode == True:
            my_barcodes.append(line[0:26])
            barcode = False
f.close()

print(my_barcodes)

with open("/home/hvose/sandbox/test_barcodes.txt", "w") as g:
    print("made the file")
    for item in my_barcodes:
        g.write(item + "\n")
g.close()