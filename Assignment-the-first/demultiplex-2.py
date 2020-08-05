#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description=" '-f' to specify filename")
parser.add_argument("-f", "--filename", help="enter output filename", required=True)
parser.add_argument("-r", "--read", help="input Read number, ex.: R1", required=True)
parser.add_argument("-l", "--read_length", help="input the read length", required=True)
args = parser.parse_args()

in_file = args.filename
read = args.read
read_len = int(args.read_length)


import gzip

def convq(c):
    p = (ord(c) - 33)
    return p

plist = [ 0 for x in range(read_len)]

#with open(in_file, "r") as f:
with gzip.open(in_file, "rt") as f:
    lc = 0                              #lc is line counter
    for line in f:
        if lc % 4 == 3:
            line = line.strip()
            for x in range(len(line)):
                plist[x] += convq(line[x])
        lc += 1




#create the averages below, by dividing plist (phred list) by the total number of records

final_list = []

for i in range(len(plist)):
    final_list.append( plist[i] / (lc / 4) )

with open(("%stnt_mean_distribution.tx" % read), "w") as out:
    astr = ''
    for item in final_list:
        astr += str(item)
        astr += " "
    out.write(read)
    out.write(astr)

#creating output graph file name
out_graph = "%s_dist.png" % read


import matplotlib.pyplot as plt

plt.figure(figsize=(10,10))

plt.xlabel("Nucleotide Position")
plt.ylabel("Mean Value Q-Score")
plt.bar(list(x for x in range(len(final_list))), final_list)
plt.show()
plt.savefig(read + "distribution.png")

